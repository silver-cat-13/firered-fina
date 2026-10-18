# Next Steps & Implementation Guide: FireRed Fina Edition

**Last Updated:** October 17, 2026  
**Target ROM:** Pokémon FireRed (USA v1.0 / `BPRE0.gba`)  
**Base ROM Path:** [`roms/1636 - Pokemon Fire Red (U)(Squirrels).gba`](file:///home/fernando/workspace/firered/firered-fina/roms/1636%20-%20Pokemon%20Fire%20Red%20(U)(Squirrels).gba)  
**Output ROM Path:** [`roms/Pokemon_FireRed_Fina_Edition.gba`](file:///home/fernando/workspace/firered/firered-fina/roms/Pokemon_FireRed_Fina_Edition.gba)  

---

## Completed Tasks Summary

* ✅ **Battle Sprites & Scale Polish:** Finita ($34 \times 45$ at $y=[16..60]$) is scaled down to adorable puppy proportions; adult Fina ($54 \times 58$ at $y=[3..60]$) looms large.
* ✅ **Party Screen Menu Icons:** Redesigned clean $32 \times 32$ pixel-art icons with native Palette 1 direct indexing and 2-frame bobbing animation.
* ✅ **Learnset Upgrades:** Removed Roar; added Blaze Kick and Hi Jump Kick to Fina (Lv 1, Lv 19, Lv 24) and Finita (Lv 19 Blaze Kick).
* ✅ **Fast Test Mode Flag:** `--test` / `-t` flag in [`scripts/patch_rom.py`](file:///home/fernando/workspace/firered/firered-fina/scripts/patch_rom.py) provides Base Friendship 220 (instant Lv 6 evolution), BST 790/970 stats, and instant kicks.
* ✅ **Python Environment:** Created [`requirements.txt`](file:///home/fernando/workspace/firered/firered-fina/requirements.txt) and [`pyproject.toml`](file:///home/fernando/workspace/firered/firered-fina/pyproject.toml).
* ✅ **Task 1: Pokédex Entry & Category Customization:** Injected Spot Pup ($0.5\text{ m}$, $12.0\text{ kg}$) and Shadowhound ($1.2\text{ m}$, $32.0\text{ kg}$) with custom Gen 3 lore descriptions.
* ✅ **Task 2: TM & HM Compatibility:** Configured 64-bit learnset bitmask for Umbreon/Absol style Dark STAB, coverage, and HMs (Cut, Strength, Flash, Rock Smash).
* ✅ **Task 3: Pokémon Cries (Audio Polish):** Re-pointed primary (`0x48C914`) and secondary (`0x48DB44`) cry tables to authentic canine cries (Eevee pup yip for Finita; Houndour hound howl for Fina).
* ✅ **Task 4: Professor Oak Starter Dialogue:** Injected custom Pallet Town lab dialogue for Pokéball #1 (`0x169C16`), offering Finita the Spot Pup Pokémon.

---

## Detailed Implementation Plan for Tasks 1–4

### 📋 Task 1: Pokédex Entry & Category Customization [RESOLVED]

#### 1. Overview & Data Structures
In Pokémon FireRed USA (BPRE v1.0), Pokédex entry metadata is stored in `gPokedexEntries` located at table offset `0x44E874`.
Each entry is exactly **36 bytes (`0x24`)**:
```c
struct PokedexEntry
{
    /*0x00*/ u8 categoryName[12];     // e.g. "SPOT PUP\0", FireRed Gen 3 text encoding, terminated with 0xFF
    /*0x0C*/ u16 height;              // In decimeters (0.1 m): 0.5m -> 5, 1.2m -> 12
    /*0x0E*/ u16 weight;              // In hectograms (0.1 kg): 12.0kg -> 120, 32.0kg -> 320
    /*0x10*/ u32 description;         // Pointer to text string (ROM address: 0x08XXXXXX)
    /*0x14*/ u16 pokemonScale;        // Pokedex screen model scale (default: 356)
    /*0x16*/ u16 pokemonOffset;       // Pokedex screen model Y offset (default: 10)
    /*0x18*/ u16 trainerScale;        // Trainer comparison scale (default: 256)
    /*0x1A*/ u16 trainerOffset;       // Trainer comparison Y offset (default: 0)
    /*0x1C*/ u32 padding[2];          // Additional camera / layout parameters
};
```

#### 2. Species Pointers & Offsets
* **Finita (Species 1 / Bulbasaur Slot):** `0x44E874 + (1 - 1) * 36 = 0x44E874`
* **Fina (Species 2 / Ivysaur Slot):** `0x44E874 + (2 - 1) * 36 = 0x44E898`

#### 3. Content Specifications
* **Finita:**
  * **Category Name:** `"SPOT PUP"` (12 bytes, uppercase, padded with `0x00` after `0xFF` terminator).
  * **Height:** `5` (`0x05, 0x00` $\rightarrow$ $0.5\text{ m}$ / $\sim 1\text{' }08\text{"}$).
  * **Weight:** `120` (`0x78, 0x00` $\rightarrow$ $12.0\text{ kg}$ / $\sim 26.4\text{ lbs}$).
  * **Description Text (FireRed Gen 3 encoding with `0xFE` newline, `0xB8` comma):**
    ```text
    A spirited, loyal Dalmatian puppy.\n
    Highly affectionate and energetic,\n
    she follows her trainer everywhere.
    ```
* **Fina:**
  * **Category Name:** `"SHADOW HOUND"` (12 bytes, uppercase).
  * **Height:** `12` (`0x0C, 0x00` $\rightarrow$ $1.2\text{ m}$ / $\sim 3\text{' }11\text{"}$).
  * **Weight:** `320` (`0x40, 0x01` $\rightarrow$ $32.0\text{ kg}$ / $\sim 70.5\text{ lbs}$).
  * **Description Text:**
    ```text
    Through a bond of friendship, she\n
    matures into a shadow guardian.\n
    Channels shadow energy to protect.
    ```

#### 4. Implementation Steps in `scripts/patch_rom.py`
1. Encode description strings using FireRed character map with linebreaks (`0xFE`) and terminator (`0xFF`).
2. Write description byte arrays to free space (e.g. `0xE46000`).
3. Update `categoryName`, `height`, `weight`, and `description` pointer at `0x44E874` and `0x44E898`.

---

### 🔮 Task 2: TM & HM Compatibility (Dark-Type Umbreon / Absol Style) [RESOLVED]

#### 1. Overview & Data Structures
In Pokémon FireRed USA, TM and HM compatibility flags are stored in `gTMHMLearnsets` at offset `OFFSET_TMHM_LEARNSETS = 0x252BC8`.
* Each entry is a **64-bit integer (8 bytes, little-endian)** per species:
  * Bits `0` through `49`: TMs 1 through 50 (`bit = TM_number - 1`).
  * Bits `50` through `57`: HMs 1 through 8 (`bit = 50 + HM_number - 1`).
* Species ID 1 (Finita) is at `0x252BC8 + 1 * 8 = 0x252BD0`.
* Species ID 2 (Fina) is at `0x252BC8 + 2 * 8 = 0x252BD8`.

#### 2. Curated Dark Pokémon Compatibility Pool
Modeled after Dark-type powerhouses like **Umbreon** and **Absol**:
* **Signature Dark STAB & Utility:**
  * TM12 Taunt (Bit 11)
  * TM41 Torment (Bit 40)
  * TM46 Thief (Bit 45)
  * TM49 Snatch (Bit 48)
* **Special & Physical Coverage:**
  * TM04 Calm Mind (Bit 3) — Counters Special Defense drops and boosts SpA.
  * TM27 Return (Bit 26) — Signature high-friendship 102 BP bond attack.
  * TM21 Frustration (Bit 20)
  * TM29 Psychic (Bit 28) — Essential coverage against Fighting weakness.
  * TM30 Shadow Ball (Bit 29) — High-power physical Ghost coverage.
  * TM23 Iron Tail (Bit 22) — Counters Rock and Fairy.
  * TM28 Dig (Bit 27) — Ground coverage.
  * TM34 Shock Wave (Bit 33) — Never-miss Electric coverage.
  * TM40 Aerial Ace (Bit 39) — Never-miss Flying coverage against Fighting.
  * TM42 Facade (Bit 41), TM43 Secret Power (Bit 42)
  * TM15 Hyper Beam (Bit 14)
* **Status, Weather & Survival:**
  * TM06 Toxic (Bit 5), TM10 Hidden Power (Bit 9), TM11 Sunny Day (Bit 10), TM17 Protect (Bit 16), TM18 Rain Dance (Bit 17), TM32 Double Team (Bit 31), TM44 Rest (Bit 43), TM45 Attract (Bit 44).
* **Field HMs:**
  * HM01 Cut (Bit 50)
  * HM04 Strength (Bit 53)
  * HM05 Flash (Bit 54)
  * HM06 Rock Smash (Bit 55)

#### 3. Bitmask Construction
```python
def build_tmhm_mask(tm_list, hm_list):
    mask = 0
    for tm in tm_list:
        mask |= (1 << (tm - 1))
    for hm in hm_list:
        mask |= (1 << (50 + hm - 1))
    return mask.to_bytes(8, 'little')
```

---

### 🔊 Task 3: Pokémon Cries (Audio Polish) [RESOLVED]

#### 1. Overview & Data Structures
In Pokémon FireRed USA, Pokémon cries use DirectSound ToneData sound headers in `gCryTable` located at `0x1CCD94`.
* Each entry is exactly **12 bytes**:
  ```c
  struct ToneData {
      u8 type;
      u8 key;
      u8 length;
      u8 pan_sweep;
      const u8 *wav;       // Pointer to 8-bit signed PCM sample
      u8 attack;
      u8 decay;
      u8 sustain;
      u8 release;
  };
  ```
* Cry IDs in Generation 3 map directly to Species IDs:
  * Bulbasaur / Finita: Cry ID `0` (`0x1CCD94 + 0 * 12 = 0x1CCD94`).
  * Ivysaur / Fina: Cry ID `1` (`0x1CCD94 + 1 * 12 = 0x1CCD94 + 12`).

#### 2. Re-pointing Canine Audio
Rather than injecting raw audio samples (which requires complex GBA sample rate conversions and sound mixer patching), FireRed has authentic canine cries:
* **Finita (Puppy):**
  * Use **Eevee (Cry ID 133)** at `0x1CCD94 + 133 * 12` or **Growlithe (Cry ID 58)** at `0x1CCD94 + 58 * 12`.
  * Eevee provides a high-pitched, playful, friendly pup yip; Growlithe provides an energetic dog bark.
* **Fina (Adult Shadow Hound):**
  * Use **Houndour (Cry ID 228)** at `0x1CCD94 + 228 * 12`.
  * Provides a deep, intimidating, authentic dark-hound growl and howl.
* **Implementation:** Copy the 12-byte `ToneData` struct from the source cry slot directly into Cry 0 and Cry 1 in `scripts/patch_rom.py`.

---

### 💬 Task 4: Professor Oak Starter Dialogue in Pallet Town [RESOLVED]

#### 1. Overview & Script Offsets
In Pallet Town's Pokémon Lab, when the player interacts with the leftmost Pokéball on Oak's table:
* Script offset: `0x169B00`–`0x169E00` (Pallet Town Lab map scripts).
* Oak triggers a confirmation prompt message box:
  * **Original Text:**
    `"So! You want the plant\nPOKéMON, BULBASAUR?"`
  * **New Text:**
    `"So! You want the SPOT PUP\nPOKéMON, FINITA?"`

#### 2. Implementation Strategy
1. Locate the text pointer in the script event at Oak's table for Pokéball #1.
2. Encode the new dialogue string in Gen 3 text format (`0xBB`–`0xEE`, `[1B]` for `é`, `0xFE` for newline, `0xFF` terminator).
3. Place the string in free space (`0xE46500`) and update the script's 4-byte pointer (`+ 0x08000000`).

---

## 🛠️ Build & Verification Toolchain

1. **Build ROM in Fast Test Mode:**
   ```bash
   .venv/bin/python scripts/patch_rom.py --test
   ```
2. **Build ROM in Release / Canonical Mode:**
   ```bash
   .venv/bin/python scripts/patch_rom.py
   ```
3. **Launch Testing in mGBA:**
   ```bash
   mgba-qt "roms/Pokemon_FireRed_Fina_Edition.gba"
   ```
