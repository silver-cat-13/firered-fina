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
OFFSET_ARTICUNO_ENCOUNTER_MSG   = 0x1631CC
OFFSET_ZAPDOS_ENCOUNTER_MSG     = 0x1637D8

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
    'Bite': 44, 'TakeDown': 36, 'FaintAttack': 185, 'Crunch': 242,
    'ConfuseRay': 109, 'Moonlight': 236, 'HiJumpKick': 136, 'BlazeKick': 299,
    # Alice moves
    'ThunderShock': 84, 'FakeOut': 252, 'Charge': 268, 'Spark': 209,
    'Screech': 103, 'ShockWave': 351, 'Slash': 163, 'Thunderbolt': 85,
    'Agility': 97, 'Thunder': 87, 'ZapCannon': 192,
    # Winter moves
    'Astonish': 310, 'Lick': 122, 'Yawn': 281, 'NightShade': 101,
    'Curse': 174, 'ShadowPunch': 325, 'Rest': 156, 'Snore': 173,
    'ShadowBall': 247, 'BodySlam': 34, 'DestinyBond': 194
}

# 1. Finita & Fina Learnsets
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

# 2. Alice Learnsets
ALICE_LEARNSET_DEFAULT = [
    (1, MOVES['QuickAttack']),
    (1, MOVES['ThunderShock']),
    (5, MOVES['FakeOut']),
    (12, MOVES['Charge']),
    (18, MOVES['Spark']),
    (25, MOVES['Screech']),
    (32, MOVES['ShockWave']),
    (39, MOVES['Slash']),
    (45, MOVES['Thunderbolt']),
    (52, MOVES['Agility']),
    (59, MOVES['Thunder']),
    (66, MOVES['ZapCannon']),
]

ALICE_LEARNSET_TEST = [
    (1, MOVES['QuickAttack']),
    (1, MOVES['Thunderbolt']),
    (1, MOVES['Agility']),
    (1, MOVES['Thunder']),
    (5, MOVES['FakeOut']),
    (6, MOVES['Thunderbolt']),
    (6, MOVES['ZapCannon']),
    (12, MOVES['Charge']),
    (18, MOVES['Spark']),
    (25, MOVES['Screech']),
    (32, MOVES['ShockWave']),
    (39, MOVES['Slash']),
    (45, MOVES['Thunderbolt']),
    (52, MOVES['Agility']),
    (59, MOVES['Thunder']),
    (66, MOVES['ZapCannon']),
]

# 3. Winter Learnsets
WINTER_LEARNSET_DEFAULT = [
    (1, MOVES['Astonish']),
    (1, MOVES['Lick']),
    (5, MOVES['Yawn']),
    (12, MOVES['NightShade']),
    (18, MOVES['ConfuseRay']),
    (25, MOVES['Curse']),
    (32, MOVES['ShadowPunch']),
    (39, MOVES['Rest']),
    (45, MOVES['Snore']),
    (52, MOVES['ShadowBall']),
    (59, MOVES['BodySlam']),
    (66, MOVES['DestinyBond']),
]

WINTER_LEARNSET_TEST = [
    (1, MOVES['Astonish']),
    (1, MOVES['ShadowBall']),
    (1, MOVES['BodySlam']),
    (1, MOVES['DestinyBond']),
    (5, MOVES['Yawn']),
    (6, MOVES['ShadowBall']),
    (6, MOVES['Rest']),
    (12, MOVES['NightShade']),
    (18, MOVES['ConfuseRay']),
    (25, MOVES['Curse']),
    (32, MOVES['ShadowPunch']),
    (39, MOVES['Rest']),
    (45, MOVES['Snore']),
    (52, MOVES['ShadowBall']),
    (59, MOVES['BodySlam']),
    (66, MOVES['DestinyBond']),
]

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

# Curated TM/HM Pools
FINITA_TM_LIST = [4, 6, 10, 11, 12, 15, 17, 18, 21, 23, 27, 28, 29, 30, 32, 34, 40, 41, 42, 43, 44, 45, 46, 49]
FINITA_HM_LIST = [1, 4, 5, 6]

ALICE_TM_LIST = [4, 6, 10, 12, 15, 16, 17, 18, 21, 23, 24, 25, 27, 28, 29, 30, 32, 33, 34, 40, 41, 42, 43, 44, 45, 46]
ALICE_HM_LIST = [1, 4, 5, 6]

WINTER_TM_LIST = [4, 6, 10, 12, 15, 17, 18, 20, 21, 23, 26, 27, 28, 29, 30, 31, 32, 36, 41, 42, 43, 44, 45, 46, 49]
WINTER_HM_LIST = [1, 4, 5, 6]

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

WINTER_DEX_DESC = (
    "A shy, sleepy cat resting in caves\\n"
    "to find peace. Loving to all life,\\n"
    "he shares a warm bond with ALICE."
)

ALICE_DEX_DESC = (
    "A playful, curious cat who loves\\n"
    "potatoes. Drawn to inventions, she\\n"
    "shares a special bond with WINTER."
)

# Dialogue text strings
OAK_STARTER_DIALOGUE = (
    "I see! FINITA is your choice.\\n"
    "It's very easy to raise.\\p"
    "So, [PLAYER], you want to go with\\n"
    "the SPOT PUP POKéMON, FINITA?"
)

ALICE_ENCOUNTER_TEXT = (
    "Nyaa-zap!\\n"
    "ALICE playfully darts around the\\l"
    "machinery with curious green eyes!\\p"
)

WINTER_ENCOUNTER_TEXT = (
    "Mroww...\\n"
    "WINTER peeks from the icy shadows,\\l"
    "softly purring with quiet warmth.\\p"
)

def patch_rom(input_rom, output_rom, test_mode=False):
    if not os.path.exists(input_rom):
        print(f"Error: Base ROM not found at {input_rom}")
        return False

    with open(input_rom, 'rb') as f:
        rom = bytearray(f.read())

    print(f"Loaded ROM: {len(rom)} bytes")
    if test_mode:
        print(">>> [TEST MODE ENABLED] Fast Evolution & High Speedrun Stats Active! <<<")
    else:
        print(">>> [NORMAL MODE] Canonical Balanced Stats Active. <<<")

    finita_id = 1   # Bulbasaur slot
    fina_id = 2     # Ivysaur slot
    winter_id = 144 # Articuno slot
    alice_id = 145  # Zapdos slot

    # 1. Write Pokemon Names
    rom[OFFSET_POKEMON_NAMES + finita_id * 11 : OFFSET_POKEMON_NAMES + (finita_id + 1) * 11] = encode_text("FINITA", max_len=10, total_len=11)
    rom[OFFSET_POKEMON_NAMES + fina_id * 11 : OFFSET_POKEMON_NAMES + (fina_id + 1) * 11] = encode_text("FINA", max_len=10, total_len=11)
    rom[OFFSET_POKEMON_NAMES + winter_id * 11 : OFFSET_POKEMON_NAMES + (winter_id + 1) * 11] = encode_text("WINTER", max_len=10, total_len=11)
    rom[OFFSET_POKEMON_NAMES + alice_id * 11 : OFFSET_POKEMON_NAMES + (alice_id + 1) * 11] = encode_text("ALICE", max_len=10, total_len=11)

    # 2. Base Stats & Configurations
    if test_mode:
        finita_stats_tup = (120, 160, 100, 150, 160, 100) # BST 790
        finita_friendship = 220
        fina_stats_tup = (150, 200, 120, 180, 200, 120)   # BST 970
        fina_friendship = 220
        winter_stats_tup = (180, 200, 200, 100, 120, 150) # BST 950
        alice_stats_tup = (120, 160, 100, 200, 200, 120)  # BST 900
    else:
        finita_stats_tup = (55, 60, 45, 55, 40, 45)       # BST 300
        finita_friendship = 70
        fina_stats_tup = (90, 80, 90, 100, 110, 80)       # BST 550
        fina_friendship = 70
        # Winter: BST 580 (focus on Atk & Def, lowest stat Speed = 50)
        winter_stats_tup = (110, 130, 135, 50, 65, 90)    # BST 580
        # Alice: BST 580 (focus on Spe & SpA, lowest stat HP = 65)
        alice_stats_tup = (65, 70, 75, 150, 140, 80)      # BST 580

    # Write Base Stats: Finita
    rom[OFFSET_BASE_STATS + finita_id * 28 : OFFSET_BASE_STATS + (finita_id + 1) * 28] = bytearray([
        *finita_stats_tup,
        0, 0,                  # Type: Normal / Normal
        255, 62,               # Catch rate, Base Exp
        0x01, 0x00,            # EV Yield (+1 Speed)
        0, 0, 0, 0,            # Held Items (None)
        254,                   # Gender: Female only
        120,                   # Hatch cycles
        finita_friendship,     # Base Friendship
        0,                     # Growth rate: Medium Fast
        5, 5,                  # Egg Group: Field
        56, 0,                 # Ability 1: Cute Charm, Ability 2: None
        0, 0, 0, 0             # Safari run rate, Color, Padding
    ])

    # Write Base Stats: Fina
    rom[OFFSET_BASE_STATS + fina_id * 28 : OFFSET_BASE_STATS + (fina_id + 1) * 28] = bytearray([
        *fina_stats_tup,
        17, 17,                # Type: Dark / Dark
        45, 210,               # Catch rate, Base Exp
        0x00, 0x04,            # EV Yield (+2 SpAtk)
        0, 0, 0, 0,            # Held Items (None)
        254,                   # Gender: Female only
        120,                   # Hatch cycles
        fina_friendship,       # Base Friendship
        0,                     # Growth rate: Medium Fast
        5, 5,                  # Egg Group: Field
        56, 0,                 # Ability 1: Cute Charm
        0, 0, 0, 0             # Padding
    ])

    # Write Base Stats: Winter (Species 144 / Articuno replacement)
    rom[OFFSET_BASE_STATS + winter_id * 28 : OFFSET_BASE_STATS + (winter_id + 1) * 28] = bytearray([
        *winter_stats_tup,
        7, 7,                  # Type: Ghost / Ghost
        3, 216,                # Catch rate: 3 (Legendary), Base Exp: 216
        0x24, 0x00,            # EV Yield: +2 Defense, +1 Attack (0x24)
        0, 0, 0, 0,            # Held Items (None)
        0,                     # Gender: Male only (0)
        120,                   # Hatch cycles
        70,                    # Base Friendship
        5,                     # Growth rate: Slow
        15, 15,                # Egg Group: Undiscovered
        23, 0,                 # Ability 1: Shadow Tag (23), Ability 2: None
        0, 0, 0, 0             # Padding
    ])

    # Write Base Stats: Alice (Species 145 / Zapdos replacement)
    rom[OFFSET_BASE_STATS + alice_id * 28 : OFFSET_BASE_STATS + (alice_id + 1) * 28] = bytearray([
        *alice_stats_tup,
        13, 13,                # Type: Electric / Electric
        3, 216,                # Catch rate: 3 (Legendary), Base Exp: 216
        0xC0, 0x00,            # EV Yield: +3 Speed (0xC0)
        0, 0, 0, 0,            # Held Items (None)
        254,                   # Gender: Female only (254)
        120,                   # Hatch cycles
        70,                    # Base Friendship
        5,                     # Growth rate: Slow
        15, 15,                # Egg Group: Undiscovered
        3, 0,                  # Ability 1: Speed Boost (3), Ability 2: None
        0, 0, 0, 0             # Padding
    ])

    # 3. Evolutions
    # Finita -> Fina via High Friendship (Method 1)
    evo_data = bytearray(40)
    evo_data[0:2] = (1).to_bytes(2, 'little')
    evo_data[2:4] = (0).to_bytes(2, 'little')
    evo_data[4:6] = (fina_id).to_bytes(2, 'little')
    rom[OFFSET_EVOLUTIONS + finita_id * 40 : OFFSET_EVOLUTIONS + (finita_id + 1) * 40] = evo_data
    # Clear Fina, Winter, Alice evolutions
    rom[OFFSET_EVOLUTIONS + fina_id * 40 : OFFSET_EVOLUTIONS + (fina_id + 1) * 40] = bytearray(40)
    rom[OFFSET_EVOLUTIONS + winter_id * 40 : OFFSET_EVOLUTIONS + (winter_id + 1) * 40] = bytearray(40)
    rom[OFFSET_EVOLUTIONS + alice_id * 40 : OFFSET_EVOLUTIONS + (alice_id + 1) * 40] = bytearray(40)

    # 4. TM & HM Compatibility
    rom[OFFSET_TMHM_LEARNSETS + finita_id * 8 : OFFSET_TMHM_LEARNSETS + (finita_id + 1) * 8] = build_tmhm_mask(FINITA_TM_LIST, FINITA_HM_LIST)
    rom[OFFSET_TMHM_LEARNSETS + fina_id * 8 : OFFSET_TMHM_LEARNSETS + (fina_id + 1) * 8] = build_tmhm_mask(FINITA_TM_LIST, FINITA_HM_LIST)
    rom[OFFSET_TMHM_LEARNSETS + winter_id * 8 : OFFSET_TMHM_LEARNSETS + (winter_id + 1) * 8] = build_tmhm_mask(WINTER_TM_LIST, WINTER_HM_LIST)
    rom[OFFSET_TMHM_LEARNSETS + alice_id * 8 : OFFSET_TMHM_LEARNSETS + (alice_id + 1) * 8] = build_tmhm_mask(ALICE_TM_LIST, ALICE_HM_LIST)
    print("TM/HM Compatibility patched successfully.")

    # 5. Pokemon Cries
    # Finita (Cry ID 0) -> Eevee (Cry ID 132)
    # Fina (Cry ID 1) -> Houndour (Cry ID 227)
    # Winter (Cry ID 143) -> Persian (Cry ID 52)
    # Alice (Cry ID 144) -> Meowth (Cry ID 51)
    eevee_cry_id = 132
    houndour_cry_id = 227
    persian_cry_id = 52
    meowth_cry_id = 51

    for table_offset in [OFFSET_CRY_TABLE, OFFSET_CRY_TABLE2]:
        eevee_tone = rom[table_offset + eevee_cry_id * 12 : table_offset + (eevee_cry_id + 1) * 12]
        houndour_tone = rom[table_offset + houndour_cry_id * 12 : table_offset + (houndour_cry_id + 1) * 12]
        persian_tone = rom[table_offset + persian_cry_id * 12 : table_offset + (persian_cry_id + 1) * 12]
        meowth_tone = rom[table_offset + meowth_cry_id * 12 : table_offset + (meowth_cry_id + 1) * 12]

        rom[table_offset + 0 * 12 : table_offset + 1 * 12] = eevee_tone
        rom[table_offset + 1 * 12 : table_offset + 2 * 12] = houndour_tone
        rom[table_offset + 143 * 12 : table_offset + 144 * 12] = persian_tone
        rom[table_offset + 144 * 12 : table_offset + 145 * 12] = meowth_tone

    print("Cries patched successfully (Finita: Eevee, Fina: Houndour, Winter: Persian, Alice: Meowth).")

    # 6. Free Space Data Allocation (starting at 0xE45000)
    free_space = 0xE45000

    # Learnsets
    if test_mode:
        finita_moves = FINITA_LEARNSET_TEST
        fina_moves = FINA_LEARNSET_TEST
        winter_moves = WINTER_LEARNSET_TEST
        alice_moves = ALICE_LEARNSET_TEST
    else:
        finita_moves = FINITA_LEARNSET_DEFAULT
        fina_moves = FINA_LEARNSET_DEFAULT
        winter_moves = WINTER_LEARNSET_DEFAULT
        alice_moves = ALICE_LEARNSET_DEFAULT

    for sid, moves in [(finita_id, finita_moves), (fina_id, fina_moves), (winter_id, winter_moves), (alice_id, alice_moves)]:
        learnset_bytes = create_learnset_bytes(moves)
        addr = free_space
        rom[addr : addr + len(learnset_bytes)] = learnset_bytes
        free_space += len(learnset_bytes)
        while free_space % 4 != 0: free_space += 1
        rom[OFFSET_LEARNSETS + sid * 4 : OFFSET_LEARNSETS + (sid + 1) * 4] = (addr + 0x08000000).to_bytes(4, 'little')

    # 7. Pokedex Descriptions & Categories
    pokedex_configs = [
        (finita_id, "SPOT PUP", 5, 120, FINITA_DEX_DESC),
        (fina_id, "SHADOWHOUND", 12, 320, FINA_DEX_DESC),
        (winter_id, "DORMANT CAT", 5, 55, WINTER_DEX_DESC),
        (alice_id, "CURIOUS CAT", 4, 42, ALICE_DEX_DESC)
    ]

    for sid, cat_name, height_dm, weight_hg, desc_text in pokedex_configs:
        desc_bytes = encode_script_string(desc_text)
        desc_addr = free_space
        rom[desc_addr : desc_addr + len(desc_bytes)] = desc_bytes
        free_space += len(desc_bytes)
        while free_space % 4 != 0: free_space += 1

        dex_entry_addr = OFFSET_POKEDEX_ENTRIES + (sid - 1) * 36
        rom[dex_entry_addr : dex_entry_addr + 12] = encode_text(cat_name, max_len=11, total_len=12)
        rom[dex_entry_addr + 12 : dex_entry_addr + 14] = (height_dm).to_bytes(2, 'little')
        rom[dex_entry_addr + 14 : dex_entry_addr + 16] = (weight_hg).to_bytes(2, 'little')
        rom[dex_entry_addr + 16 : dex_entry_addr + 20] = (desc_addr + 0x08000000).to_bytes(4, 'little')

    print("Pokedex entries & categories patched successfully.")

    # 8. Script Dialogues (Starter + Legendary Encounters)
    dialogues = [
        (OFFSET_OAK_POKEBALL1_TEXT_PTR, OAK_STARTER_DIALOGUE),
        (OFFSET_ARTICUNO_ENCOUNTER_MSG, WINTER_ENCOUNTER_TEXT),
        (OFFSET_ZAPDOS_ENCOUNTER_MSG, ALICE_ENCOUNTER_TEXT)
    ]

    for ptr_offset, dialogue_text in dialogues:
        dlg_bytes = encode_script_string(dialogue_text)
        dlg_addr = free_space
        rom[dlg_addr : dlg_addr + len(dlg_bytes)] = dlg_bytes
        free_space += len(dlg_bytes)
        while free_space % 4 != 0: free_space += 1
        rom[ptr_offset : ptr_offset + 4] = (dlg_addr + 0x08000000).to_bytes(4, 'little')

    print("Starter dialogue and wild legendary encounter dialogues patched successfully.")

    # Write Output ROM
    with open(output_rom, 'wb') as f:
        f.write(rom)

    print(f"Stats, learnsets, pokedex, TM/HM, cries & dialogues patched successfully.")
    print(f"Now inserting sprites, palettes, icons, and overworld graphics...")
    apply_sprites_to_rom(output_rom)
    return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Patch Pokémon FireRed with Finita, Fina, Winter, and Alice custom species.")
    parser.add_argument("--test", "-t", action="store_true", help="Enable fast test mode: boosted stats, instant Lv 6 friendship evolution, early moves")
    parser.add_argument("--in-rom", default="roms/1636 - Pokemon Fire Red (U)(Squirrels).gba", help="Path to clean base FireRed ROM")
    parser.add_argument("--out-rom", default="roms/Pokemon_FireRed_Fina_Edition.gba", help="Path to output modified ROM")
    args = parser.parse_args()

    patch_rom(args.in_rom, args.out_rom, test_mode=args.test)
