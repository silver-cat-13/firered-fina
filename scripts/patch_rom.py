import sys
import os
from PIL import Image

# Import sprite patcher
from patch_sprites import apply_sprites_to_rom

# FireRed USA v1.0 (BPRE) Table Offsets
OFFSET_BASE_STATS = 0x254784
OFFSET_EVOLUTIONS = 0x25D000
OFFSET_LEARNSETS  = 0x25D7B4
OFFSET_POKEMON_NAMES = 0x245EE0

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
    ' ': 0x00, '-': 0xE3, '.': 0xAD, '!': 0xAB, '?': 0xAC
}

def encode_text(text, max_len=10):
    encoded = bytearray()
    for char in text[:max_len]:
        encoded.append(CHAR_MAP.get(char, 0x00))
    encoded.append(0xFF) # Terminator
    while len(encoded) < 11:
        encoded.append(0x00)
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

    # Write Pokemon Names
    rom[OFFSET_POKEMON_NAMES + finita_id * 11 : OFFSET_POKEMON_NAMES + (finita_id + 1) * 11] = encode_text("FINITA")
    rom[OFFSET_POKEMON_NAMES + fina_id * 11 : OFFSET_POKEMON_NAMES + (fina_id + 1) * 11] = encode_text("FINA")

    # Base Stats & Friendship Configuration
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

    # Write Evolution: Finita -> Fina via High Friendship (Method 1)
    evo_data = bytearray(40)
    evo_data[0:2] = (1).to_bytes(2, 'little')
    evo_data[2:4] = (0).to_bytes(2, 'little')
    evo_data[4:6] = (fina_id).to_bytes(2, 'little')
    rom[OFFSET_EVOLUTIONS + finita_id * 40 : OFFSET_EVOLUTIONS + (finita_id + 1) * 40] = evo_data

    # Select Learnsets based on mode
    if test_mode:
        finita_moves = FINITA_LEARNSET_TEST
        fina_moves = FINA_LEARNSET_TEST
    else:
        finita_moves = FINITA_LEARNSET_DEFAULT
        fina_moves = FINA_LEARNSET_DEFAULT

    finita_learnset_data = create_learnset_bytes(finita_moves)
    fina_learnset_data = create_learnset_bytes(fina_moves)

    # Write Move Learnset to Free Space (0xE45000)
    free_space = 0xE45000

    # Finita Learnset Pointer
    finita_learnset_addr = free_space
    rom[finita_learnset_addr : finita_learnset_addr + len(finita_learnset_data)] = finita_learnset_data
    free_space += len(finita_learnset_data)
    while free_space % 4 != 0: free_space += 1

    # Fina Learnset Pointer
    fina_learnset_addr = free_space
    rom[fina_learnset_addr : fina_learnset_addr + len(fina_learnset_data)] = fina_learnset_data
    free_space += len(fina_learnset_data)
    while free_space % 4 != 0: free_space += 1

    # Update Learnset Table Pointers
    rom[OFFSET_LEARNSETS + finita_id * 4 : OFFSET_LEARNSETS + (finita_id + 1) * 4] = (finita_learnset_addr + 0x08000000).to_bytes(4, 'little')
    rom[OFFSET_LEARNSETS + fina_id * 4 : OFFSET_LEARNSETS + (fina_id + 1) * 4] = (fina_learnset_addr + 0x08000000).to_bytes(4, 'little')

    # Write Output ROM
    with open(output_rom, 'wb') as f:
        f.write(rom)

    print(f"Stats, learnsets & evolutions patched successfully. Now inserting sprites and party icons...")
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
