# Finita & Fina: Pokémon Design & Stats

This project is a custom gift, bringing a real Dalmatian dog, **Finita**, into *Pokémon FireRed* as his starting partner, and watching her grow into **Fina**.

---

## Concept & Story

* **Finita (The Spot Pup):** An energetic, loyal Dalmatian puppy who follows her trainer everywhere. She starts off playful and spirited, keeping her trainer company from the very start of the journey in Pallet Town.
* **Fina (The Shadow Guardian):** As her bond with her trainer deepens, Finita matures into Fina. She channels shadow energy to protect her trainer, sporting sleek midnight markings while keeping her warm, loving personality.

---

## Visual Design & Features

> For full technical sprite specs, color palettes, and file paths, check out [`docs/sprites.md`](file:///home/fernando/workspace/firered/firered-fina/docs/sprites.md).

### 1. Finita (Puppy Form)
* **Look & Feel:** Cute puppy proportions with floppy ears, chubby paws, and a bouncing stance.
* **Distinct Markings:** Soft Dalmatian spots, including her signature spot patch over her left eye and chest spots based on real photos of Finita.
* **Expression:** Big, bright eyes with a happy grin or pink tongue sticking out.
* **Files:** `assets/sprites/finita_front.png`, `assets/sprites/finita_back.png`, `assets/sprites/finita_shiny.png`, `assets/icons/finita_icon.png`

### 2. Fina (Adult Evolution)
* **Look & Feel:** Sleek, athletic adult hound posture—graceful and alert.
* **Shadow Motif:** Midnight "socks" on her paws, dark slate ear tips, subtle shadow aura, and her signature eye patch.
* **Expression:** Warm amber eyes with a clever, confident smile.
* **Files:** `assets/sprites/fina_front.png`, `assets/sprites/fina_back.png`, `assets/sprites/fina_shiny.png`, `assets/icons/fina_icon.png`

---

## Evolution Requirement

Finita evolves into Fina through **High Friendship (`Friendship >= 220`) upon leveling up**. This reflects the bond built over the course of the journey.

*In Hex Maniac Advance (HMA): Evolution Method = `HighFriendship`, Argument = `0`, Target = `SPECIES_FINA`.*

---

## Base Stats & Battle Roles

### Finita (Normal Type)
* **Role:** Early-game starter replacement
* **Ability:** Cute Charm
* **Base Stat Total:** 300

| Stat | Value | Notes |
| :--- | :---: | :--- |
| **HP** | 55 | Good early survivability |
| **Attack** | 60 | Solid physical tackle power |
| **Defense** | 45 | Playful puppy defenses |
| **Sp. Atk** | 40 | Modest special power |
| **Sp. Def** | 45 | Decent early bulk |
| **Speed** | 55 | Nimble and quick on her feet |

---

### Fina (Dark Type)
* **Role:** Late-game guardian & powerhouse
* **Ability:** Cute Charm
* **Base Stat Total:** 550

| Stat | Value | Notes |
| :--- | :---: | :--- |
| **HP** | 90 | Great overall bulk |
| **Attack** | 80 | Capable physical coverage |
| **Defense** | 90 | Sturdy physical guard |
| **Sp. Atk** | 110 | Hits hard with Gen 3 Dark attacks |
| **Sp. Def** | 80 | Reliable special protection |
| **Speed** | 100 | Fast pack-hunter speed tier |

> **Gen 3 Battle Note:** In Generation 3, Dark-type moves (*Bite*, *Crunch*, *Faint Attack*) use Special Attack, making Fina's 110 Sp. Atk hit very hard. Her 80 Physical Attack gives great secondary utility for moves like *Return* and *Shadow Ball*.

---

## Level-Up Learnset

### Finita (Base Form)
| Level | Move | Type | Category (Gen 3) | Power | Acc | PP | Notes |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **1** | Tackle | Normal | Physical | 35 | 95% | 35 | Starting move |
| **1** | Tail Whip | Normal | Status | — | 100% | 30 | Lowers target Defense |
| **5** | Charm | Normal | Status | — | 100% | 20 | Sharply lowers target Attack |
| **9** | Quick Attack | Normal | Physical | 40 | 100% | 30 | Priority (+1) |
| **14** | Bite | Dark | Special | 60 | 100% | 25 | 30% flinch chance |
| **19** | Blaze Kick | Fire | Special | 85 | 90% | 10 | High crit ratio, 10% burn |
| **24** | Take Down | Normal | Physical | 90 | 85% | 20 | Heavy physical tackle |
| **29** | Faint Attack | Dark | Special | 60 | — | 20 | Never misses |
| **35** | Crunch | Dark | Special | 80 | 100% | 15 | Heavy attack (20% Sp. Def drop) |
| **42** | Confuse Ray | Ghost | Status | — | 100% | 10 | 100% accurate confusion |
| **52** | Moonlight | Normal | Status | — | — | 5 | Restores 50% max HP |

### Fina (Adult Shadow Guardian)
| Level | Move | Type | Category (Gen 3) | Power | Acc | PP | Notes |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **1** | Tackle | Normal | Physical | 35 | 95% | 35 | Starting move |
| **1** | Tail Whip | Normal | Status | — | 100% | 30 | Lowers target Defense |
| **1 / 19** | Blaze Kick | Fire | Special | 85 | 90% | 10 | High crit ratio, 10% burn, leverages 110 SpA |
| **1 / 24** | Hi Jump Kick | Fighting | Physical | 85 | 90% | 20 | Fighting coverage, leverages 80 Atk |
| **5** | Charm | Normal | Status | — | 100% | 20 | Sharply lowers target Attack |
| **9** | Quick Attack | Normal | Physical | 40 | 100% | 30 | Priority (+1) |
| **14** | Bite | Dark | Special | 60 | 100% | 25 | STAB (30% flinch) |
| **29** | Faint Attack | Dark | Special | 60 | — | 20 | STAB; never misses |
| **35** | Crunch | Dark | Special | 80 | 100% | 15 | Heavy STAB (20% Sp. Def drop) |
| **42** | Confuse Ray | Ghost | Status | — | 100% | 10 | 100% accurate confusion |
| **52** | Moonlight | Normal | Status | — | — | 5 | Restores 50% max HP |

*(Note: Roar has been permanently removed from both learnsets).*

---

### Fast Testing Mode (`--test`)
Running `python3 scripts/patch_rom.py --test` builds the ROM with speedrun testing values:
* **Instant Evolution:** Finita Base Friendship set to `220` (evolves into Fina immediately on Level 5 $\rightarrow$ Level 6).
* **Speedrun Stats:** Finita BST `790` (120/160/100/150/160/100) and Fina BST `970` (150/200/120/180/200/120).
* **Early Testing Attacks:** Blaze Kick and Hi Jump Kick are unlocked at Level 1 and Level 6 for rapid testing.

---

## TM & HM Compatibility

Finita and Fina can learn the following TMs and HMs:

* **Key STAB & Coverage TMs:**
  * **TM27 Return:** Signature bond attack (102 BP at max friendship).
  * **TM29 Psychic:** Strong Special attack that counters Fina's Fighting-type weakness.
  * **TM30 Shadow Ball:** High-power physical Ghost move.
  * **TM04 Calm Mind:** Boosts Sp. Atk and Sp. Def.
  * **TM12 Taunt / TM41 Torment / TM46 Thief:** Utility Dark-type moves.
* **Field HMs:**
  * **HM01 Cut**, **HM04 Strength**, **HM05 Flash**