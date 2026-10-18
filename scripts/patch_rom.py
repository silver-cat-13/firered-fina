import sys
import os
import struct
from PIL import Image

# Import sprite patcher
from patch_sprites import apply_sprites_to_rom

# FireRed USA v1.0 (BPRE) Table Offsets
OFFSET_BASE_STATS               = 0x254784
OFFSET_EVOLUTIONS               = 0x259754
OFFSET_LEARNSETS                = 0x25D7B4
OFFSET_POKEMON_NAMES            = 0x245EE0
OFFSET_POKEDEX_ENTRIES          = 0x44E874
OFFSET_TMHM_LEARNSETS           = 0x252BC8
OFFSET_CRY_TABLE                = 0x48C914
OFFSET_CRY_TABLE2               = 0x48DB44
OFFSET_OAK_POKEBALL1_TEXT_PTR   = 0x169C16

# Gen 3 Text Encoder for FireRed
CHAR_MAP = {
    'A': 0xBB, 'B': 0xBC, 'C': 0xBD, 'D': 0xBE, 'E': 0xBF, 'F': 0xC0, 'G': 0xC1,
    'H': 0xC2, 'I': 0xC3, 'J': 0xC4, 'K': 0xC5, 'L': 0xC6, 'M': 0xC7, 'N': 0xC8,
    'O': 0xC9, 'P': 0xCA, 'Q': 0xCB, 'R': 0xCC, 'S': 0xCD, 'T': 0xCE, 'U': 0xCF,
    'V': 0xD0, 'W': 0xD1, 'X': 0xD2, 'Y': 0xD3, 'Z': 0xD4,
    'a': 0xD5, 'b': 0xD6, 'c': 0xD7, 'd': 0xD8, 'e': 0xD9, 'f': 0xDA, 'g': 0xDB,
    'h': 0xDC, 'i': 0xDD, 'j': 0xDE, 'k': 0xDF, 'l': 0xE0, 'm': 0xE1, 'n': 0xE2,
    'o': 0xE3, 'p': 0xE4, 'q': 0xE5, 'r': 0xE6, 's': 0xE7, 't': 0xE8, 'u': 0xE9,
    'v': 0xEA, 'w': 0xEB, 'x': 0xEC, 'y': 0xED, 'z': 0xEE,
    '0': 0xA1, '1': 0xA2, '2': 0xA3, '3': 0xA4, '4': 0xA5,
    '5': 0xA6, '6': 0xA7, '7': 0xA8, '8': 0xA9, '9': 0xAA,
    ' ': 0x00, '-': 0xAE, '.': 0xAD, '!': 0xAB, '?': 0xAC,
    ',': 0xB8, "'": 0xB4, '’': 0xB4, 'é': 0x1B, ':': 0xF0
}

def encode_text(text, max_len=10, total_len=11):
    """Encode fixed-length strings like Pokemon Names or Categories with 0xFF terminator and 0x00 padding."""
    encoded = bytearray()
    for char in text[:max_len]:
        encoded.append(CHAR_MAP.get(char, 0x00))
    encoded.append(0xFF) # Terminator
    while len(encoded) < total_len:
        encoded.append(0x00)
    return bytes(encoded[:total_len])

def encode_script_string(text):
    """Encode variable-length strings supporting control codes like \\n, \\l, \\p, and [PLAYER]."""
    encoded = bytearray()
    i = 0
    while i < len(text):
        if text[i:i+2] == '\\n':
            encoded.append(0xFE)
            i += 2
        elif text[i:i+2] == '\\l':
            encoded.append(0xFA)
            i += 2
        elif text[i:i+2] == '\\p':
            encoded.append(0xFB)
            i += 2
        elif text[i:i+8] == '[PLAYER]':
            encoded.extend([0xFD, 0x01])
            i += 8
        elif text[i] == '\n':
            encoded.append(0xFE)
            i += 1
        elif text[i] in CHAR_MAP:
            encoded.append(CHAR_MAP[text[i]])
            i += 1
        else:
            encoded.append(0x00)
            i += 1
    encoded.append(0xFF) # End of string marker
    return bytes(encoded)

# Move IDs in FireRed
MOVES = {
    'Tackle': 33, 'TailWhip': 39, 'Charm': 204, 'QuickAttack': 98,
    'Bite': 44, 'Roar': 46, 'TakeDown': 36, 'FaintAttack': 185,
    'Crunch': 242, 'ConfuseRay': 109, 'Moonlight': 236,
    'HiJumpKick': 136, 'BlazeKick': 299
}

# Standard Learnsets (Roar removed, Fina learns Blaze Kick & Hi Jump Kick)
FINITA_LEARNSET_DEFAULT = [
    (1, MOVES['Tackle']),
    (1, MOVES['TailWhip']),
    (5, MOVES['Charm']),
    (9, MOVES['QuickAttack']),
    (14, MOVES['Bite']),
    (19, MOVES['BlazeKick']),
    (24, MOVES['TakeDown']),
    (29, MOVES['FaintAttack']),
    (35, MOVES['Crunch']),
    (42, MOVES['ConfuseRay']),
    (52, MOVES['Moonlight']),
]

FINA_LEARNSET_DEFAULT = [
    (1, MOVES['Tackle']),
    (1, MOVES['TailWhip']),
    (1, MOVES['BlazeKick']),
    (1, MOVES['HiJumpKick']),
    (5, MOVES['Charm']),
    (9, MOVES['QuickAttack']),
    (14, MOVES['Bite']),
    (19, MOVES['BlazeKick']),
    (24, MOVES['HiJumpKick']),
    (29, MOVES['FaintAttack']),
    (35, MOVES['Crunch']),
    (42, MOVES['ConfuseRay']),
    (52, MOVES['Moonlight']),
]

# Fast Testing Learnsets (Blaze Kick & Hi Jump Kick available from Lv 1 & Lv 6)
FINITA_LEARNSET_TEST = [
    (1, MOVES['Tackle']),
    (1, MOVES['TailWhip']),
    (1, MOVES['BlazeKick']),
    (1, MOVES['HiJumpKick']),
    (5, MOVES['Charm']),
    (6, MOVES['BlazeKick']),
    (6, MOVES['HiJumpKick']),
    (9, MOVES['QuickAttack']),
    (14, MOVES['Bite']),
    (19, MOVES['BlazeKick']),
    (24, MOVES['HiJumpKick']),
    (29, MOVES['FaintAttack']),
    (35, MOVES['Crunch']),
    (42, MOVES['ConfuseRay']),
    (52, MOVES['Moonlight']),
]

FINA_LEARNSET_TEST = FINITA_LEARNSET_TEST

def create_learnset_bytes(moves_list):
    data = bytearray()
    for lvl, move_id in moves_list:
        val = (lvl << 9) | (move_id & 0x1FF)
        data.extend(val.to_bytes(2, 'little'))
    data.extend((0xFFFF).to_bytes(2, 'little')) # End marker
    return bytes(data)

def build_tmhm_mask(tm_list, hm_list):
    """Builds a 64-bit little-endian bitmask for TM & HM compatibility."""
    mask = 0
    for tm in tm_list:
        mask |= (1 << (tm - 1))
    for hm in hm_list:
        mask |= (1 << (50 + hm - 1))
    return mask.to_bytes(8, 'little')

# Curated Dark-type TM & HM compatibility pool (Umbreon / Absol style)
TM_LIST = [4, 6, 10, 11, 12, 15, 17, 18, 21, 23, 27, 28, 29, 30, 32, 34, 40, 41, 42, 43, 44, 45, 46, 49]
HM_LIST = [1, 4, 5, 6]

# Pokedex Descriptions
FINITA_DEX_DESC = (
    "A spirited, loyal Dalmatian puppy.\\n"
    "Highly affectionate and energetic,\\n"
    "she follows her trainer everywhere."
)

FINA_DEX_DESC = (
    "Through a bond of friendship, she\\n"
    "matures into a shadow guardian.\\n"
    "Channels shadow energy to protect."
)

# Professor Oak Starter Dialogue (Leftmost Pokeball #1)
OAK_STARTER_DIALOGUE = (
    "I see! FINITA is your choice.\\n"
    "It's very easy to raise.\\p"
    "So, [PLAYER], you want to go with\\n"
    "the SPOT PUP POKéMON, FINITA?"
)

def patch_rom(input_rom, output_rom, test_mode=False):
    if not os.path.exists(input_rom):
        print(f"Error: Base ROM not found at {input_rom}")
        return False

    with open(input_rom, 'rb') as f:
        rom = bytearray(f.read())

    print(f"Loaded ROM: {len(rom)} bytes")
    if test_mode:
        print(">>> [TEST MODE ENABLED] Fast Evolution (Base Friendship = 220), Boosted Stats (BST 790/970), and Instant Kicks (Blaze Kick & Hi Jump Kick) active! <<<")
    else:
        print(">>> [NORMAL MODE] Canonical Stats (BST 300/550), Standard Friendship (70), and Progressive Learnset active. <<<")

    finita_id = 1 # Bulbasaur slot
    fina_id = 2   # Ivysaur slot

    # 1. Write Pokemon Names
    rom[OFFSET_POKEMON_NAMES + finita_id * 11 : OFFSET_POKEMON_NAMES + (finita_id + 1) * 11] = encode_text("FINITA", max_len=10, total_len=11)
    rom[OFFSET_POKEMON_NAMES + fina_id * 11 : OFFSET_POKEMON_NAMES + (fina_id + 1) * 11] = encode_text("FINA", max_len=10, total_len=11)

    # 2. Base Stats & Friendship Configuration
    if test_mode:
        # Boosted stats for fast speedrunning/testing: HP, Atk, Def, Spe, SpA, SpD
        finita_hp, finita_atk, finita_def, finita_spe, finita_spa, finita_spd = 120, 160, 100, 150, 160, 100
        finita_friendship = 220 # Evolves into Fina immediately on first level-up (e.g. Lv 5 -> Lv 6)
        
        fina_hp, fina_atk, fina_def, fina_spe, fina_spa, fina_spd = 150, 200, 120, 180, 200, 120
        fina_friendship = 220
    else:
        # Canonical Balanced Stats
        finita_hp, finita_atk, finita_def, finita_spe, finita_spa, finita_spd = 55, 60, 45, 55, 40, 45
        finita_friendship = 70
        
        fina_hp, fina_atk, fina_def, fina_spe, fina_spa, fina_spd = 90, 80, 90, 100, 110, 80
        fina_friendship = 70

    # Write Base Stats: Finita
    finita_stats = bytearray([
        finita_hp, finita_atk, finita_def, finita_spe, finita_spa, finita_spd, # Base Stats
        0, 0,                  # Normal / Normal
        255, 62,               # Catch rate, Base Exp
        0x01, 0x00,            # EV Yield (+1 Speed)
        0, 0, 0, 0,            # Held Items (None)
        254,                   # Gender: Female only
        120,                   # Hatch cycles
        finita_friendship,     # Base Friendship (220 for instant test evolution, 70 normal)
        0,                     # Growth rate: Medium Fast
        5, 5,                  # Egg Group: Field
        56, 0,                 # Ability 1: Cute Charm, Ability 2: None
        0, 0, 0, 0             # Safari run rate, Color, Padding
    ])
    rom[OFFSET_BASE_STATS + finita_id * 28 : OFFSET_BASE_STATS + (finita_id + 1) * 28] = finita_stats

    # Write Base Stats: Fina
    fina_stats = bytearray([
        fina_hp, fina_atk, fina_def, fina_spe, fina_spa, fina_spd, # Base Stats
        17, 17,                  # Dark / Dark
        45, 210,                 # Catch rate, Base Exp
        0x00, 0x04,              # EV Yield (+2 SpAtk)
        0, 0, 0, 0,              # Held Items (None)
        254,                     # Gender: Female only
        120,                     # Hatch cycles
        fina_friendship,         # Base Friendship
        0,                       # Growth rate: Medium Fast
        5, 5,                    # Egg Group: Field
        56, 0,                   # Ability 1: Cute Charm
        0, 0, 0, 0               # Padding
    ])
    rom[OFFSET_BASE_STATS + fina_id * 28 : OFFSET_BASE_STATS + (fina_id + 1) * 28] = fina_stats

    # 3. Write Evolution: Finita -> Fina via High Friendship (Method 1)
    evo_data = bytearray(40)
    evo_data[0:2] = (1).to_bytes(2, 'little')
    evo_data[2:4] = (0).to_bytes(2, 'little')
    evo_data[4:6] = (fina_id).to_bytes(2, 'little')
    rom[OFFSET_EVOLUTIONS + finita_id * 40 : OFFSET_EVOLUTIONS + (finita_id + 1) * 40] = evo_data
    # Clear Fina evolutions (Fina is the final guardian form; do not evolve into Venusaur)
    rom[OFFSET_EVOLUTIONS + fina_id * 40 : OFFSET_EVOLUTIONS + (fina_id + 1) * 40] = bytearray(40)

    # 4. TM & HM Compatibility (Task 2)
    tmhm_bytes = build_tmhm_mask(TM_LIST, HM_LIST)
    rom[OFFSET_TMHM_LEARNSETS + finita_id * 8 : OFFSET_TMHM_LEARNSETS + (finita_id + 1) * 8] = tmhm_bytes
    rom[OFFSET_TMHM_LEARNSETS + fina_id * 8 : OFFSET_TMHM_LEARNSETS + (fina_id + 1) * 8] = tmhm_bytes
    print("TM/HM Compatibility patched successfully (Dark-type Umbreon/Absol pool).")

    # 5. Pokemon Cries (Task 3)
    # Finita (Cry ID 0) -> Eevee (Cry ID 132 in cry tables)
    # Fina (Cry ID 1) -> Houndour (Cry ID 227 in cry tables)
    eevee_cry_id = 132
    houndour_cry_id = 227

    for table_offset, table_name in [(OFFSET_CRY_TABLE, "Primary"), (OFFSET_CRY_TABLE2, "Secondary")]:
        eevee_tone = rom[table_offset + eevee_cry_id * 12 : table_offset + (eevee_cry_id + 1) * 12]
        houndour_tone = rom[table_offset + houndour_cry_id * 12 : table_offset + (houndour_cry_id + 1) * 12]

        # Apply to Finita (Cry 0) and Fina (Cry 1)
        rom[table_offset + 0 * 12 : table_offset + 1 * 12] = eevee_tone
        rom[table_offset + 1 * 12 : table_offset + 2 * 12] = houndour_tone

    print("Canine cries patched successfully (Finita -> Eevee yip, Fina -> Houndour howl).")

    # 6. Free Space Data Allocation (starting at 0xE45000)
    free_space = 0xE45000

    # Learnsets
    if test_mode:
        finita_moves = FINITA_LEARNSET_TEST
        fina_moves = FINA_LEARNSET_TEST
    else:
        finita_moves = FINITA_LEARNSET_DEFAULT
        fina_moves = FINA_LEARNSET_DEFAULT

    finita_learnset_data = create_learnset_bytes(finita_moves)
    fina_learnset_data = create_learnset_bytes(fina_moves)

    finita_learnset_addr = free_space
    rom[finita_learnset_addr : finita_learnset_addr + len(finita_learnset_data)] = finita_learnset_data
    free_space += len(finita_learnset_data)
    while free_space % 4 != 0: free_space += 1

    fina_learnset_addr = free_space
    rom[fina_learnset_addr : fina_learnset_addr + len(fina_learnset_data)] = fina_learnset_data
    free_space += len(fina_learnset_data)
    while free_space % 4 != 0: free_space += 1

    # Update Learnset Table Pointers
    rom[OFFSET_LEARNSETS + finita_id * 4 : OFFSET_LEARNSETS + (finita_id + 1) * 4] = (finita_learnset_addr + 0x08000000).to_bytes(4, 'little')
    rom[OFFSET_LEARNSETS + fina_id * 4 : OFFSET_LEARNSETS + (fina_id + 1) * 4] = (fina_learnset_addr + 0x08000000).to_bytes(4, 'little')

    # 7. Pokedex Descriptions & Categories (Task 1)
    finita_desc_bytes = encode_script_string(FINITA_DEX_DESC)
    fina_desc_bytes = encode_script_string(FININA_DEX_DESC if 'FININA_DEX_DESC' in locals() else FINA_DEX_DESC)

    finita_desc_addr = free_space
    rom[finita_desc_addr : finita_desc_addr + len(finita_desc_bytes)] = finita_desc_bytes
    free_space += len(finita_desc_bytes)
    while free_space % 4 != 0: free_space += 1

    fina_desc_addr = free_space
    rom[fina_desc_addr : fina_desc_addr + len(fina_desc_bytes)] = fina_desc_bytes
    free_space += len(fina_desc_bytes)
    while free_space % 4 != 0: free_space += 1

    # Finita Pokedex Entry (species ID 1)
    dex_finita_addr = OFFSET_POKEDEX_ENTRIES + (finita_id - 1) * 36
    rom[dex_finita_addr : dex_finita_addr + 12] = encode_text("SPOT PUP", max_len=11, total_len=12)
    rom[dex_finita_addr + 12 : dex_finita_addr + 14] = (5).to_bytes(2, 'little')     # 0.5 m
    rom[dex_finita_addr + 14 : dex_finita_addr + 16] = (120).to_bytes(2, 'little')   # 12.0 kg
    rom[dex_finita_addr + 16 : dex_finita_addr + 20] = (finita_desc_addr + 0x08000000).to_bytes(4, 'little')

    # Fina Pokedex Entry (species ID 2)
    dex_fina_addr = OFFSET_POKEDEX_ENTRIES + (fina_id - 1) * 36
    rom[dex_fina_addr : dex_fina_addr + 12] = encode_text("SHADOWHOUND", max_len=11, total_len=12)
    rom[dex_fina_addr + 12 : dex_fina_addr + 14] = (12).to_bytes(2, 'little')       # 1.2 m
    rom[dex_fina_addr + 14 : dex_fina_addr + 16] = (320).to_bytes(2, 'little')      # 32.0 kg
    rom[dex_fina_addr + 16 : dex_fina_addr + 20] = (fina_desc_addr + 0x08000000).to_bytes(4, 'little')

    print("Pokedex entries & categories patched successfully (Finita: Spot Pup, Fina: Shadowhound).")

    # 8. Professor Oak Starter Dialogue (Task 4)
    oak_dialogue_bytes = encode_script_string(OAK_STARTER_DIALOGUE)
    oak_dialogue_addr = free_space
    rom[oak_dialogue_addr : oak_dialogue_addr + len(oak_dialogue_bytes)] = oak_dialogue_bytes
    free_space += len(oak_dialogue_bytes)
    while free_space % 4 != 0: free_space += 1

    # Update Oak table script pointer
    rom[OFFSET_OAK_POKEBALL1_TEXT_PTR : OFFSET_OAK_POKEBALL1_TEXT_PTR + 4] = (oak_dialogue_addr + 0x08000000).to_bytes(4, 'little')
    print("Professor Oak starter dialogue patched successfully.")

    # Write Output ROM
    with open(output_rom, 'wb') as f:
        f.write(rom)

    print(f"Stats, learnsets, pokedex, TM/HM, cries & Oak dialogue patched successfully.")
    print(f"Now inserting sprites and party icons...")
    apply_sprites_to_rom(output_rom)
    return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Patch Pokémon FireRed with Finita & Fina custom species.")
    parser.add_argument("--test", "-t", action="store_true", help="Enable fast test mode: boosted stats, instant Lv 6 friendship evolution, early Blaze Kick & Hi Jump Kick")
    parser.add_argument("--in-rom", default="roms/1636 - Pokemon Fire Red (U)(Squirrels).gba", help="Path to clean base FireRed ROM")
    parser.add_argument("--out-rom", default="roms/Pokemon_FireRed_Fina_Edition.gba", help="Path to output modified ROM")
    args = parser.parse_args()

    patch_rom(args.in_rom, args.out_rom, test_mode=args.test)
