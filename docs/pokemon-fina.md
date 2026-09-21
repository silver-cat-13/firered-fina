# Pokémon Design: Finita & Fina

## Concept & Lore
- **Base Form (Finita):** The Spot Pup Pokémon. A spirited, loyal Dalmatian puppy. Highly affectionate, energetic, and alert, she follows her trainer everywhere.
- **Evolution (Fina):** The Shadow Hound Pokémon. Through a deep bond of friendship, she matures into an elegant, loyal Dalmatian guardian. While she embraces Dark-type power, she retains her cute, loving dog essence—channeling shadow energy through sleek midnight markings and nocturnal grace rather than ferocity.

---

## Visual Design & Sprite Direction

### 1. Finita (Base Puppy Form)
- **Silhouette:** Playful puppy proportions—slightly oversized floppy ears, chubby paws, and a bouncing stance.
- **Canvas Size:** Centered within ~48x48 pixels inside the 64x64 frame.
- **Markings:** Soft, scattered Dalmatian spots; bright puppy eyes with large specular highlights.
- **Expression:** Wide, innocent gaze with an open smile or pink tongue out.

### 2. Fina (Adult Evolution — Cute Dark Type)
- **Silhouette:** Sleek, athletic adult Dalmatian with graceful, curved posture (reminiscent of Umbreon or Houndour, avoiding bulky or monstrous builds).
- **Canvas Size:** Fills ~58x58 pixels inside the 64x64 frame.
- **Dark-Type Motif:**
  - Midnight-black/plum "socks" on her paws.
  - Soft crescent-shaped eye patch over one eye.
  - Floppy ears with tips fading gently into midnight slate.
  - Retains a clean, spotted Dalmatian coat rather than jagged edges or claws.
- **Expression:** Warm, clever grin; bright amber/honey-gold eyes with highlights that preserve her adorable, companion charm.

---

## Evolution Method
- **Trigger:** High Friendship (`Friendship >= 220`) + Level Up.
- *(In HMA / Hex Maniac Advance: Method = `Friendship`, Argument = `0`, Target = `SPECIES_FINA`)*

---

## 1. Base Form: Finita

- **Typing:** `Normal`
- **Abilities:**
  - Ability 1: `Cute Charm`
- **Base Stat Total (BST):** 300

| Stat | Value | Role / Notes |
| :--- | :---: | :--- |
| **HP** | 55 | Decent early survivability |
| **Attack** | 60 | Solid physical hitting power |
| **Defense** | 45 | Fragile puppy defenses |
| **Sp. Atk** | 40 | Low special capability |
| **Sp. Def** | 45 | Standard early-game bulk |
| **Speed** | 55 | Quick on her feet |

---

## 2. Evolved Form: Fina

- **Typing:** `Dark`
  - *Gen 3 Resistances & Immunities:*
    - Immune to **Psychic**
    - Resists **Dark** and **Ghost**
    - Weak to **Bug** (2x) and **Fighting** (2x)
- **Abilities:**
  - Ability 1: `Cute Charm`
- **Base Stat Total (BST):** 550 (Late-game powerhouse)

| Stat | Value | Role / Notes |
| :--- | :---: | :--- |
| **HP** | 90 | Sturdy companion bulk |
| **Attack** | 80 | Capable physical coverage |
| **Defense** | 90 | Reliable physical guard |
| **Sp. Atk** | 110 | Strong Special Attack for Gen 3 Dark attacks |
| **Sp. Def** | 80 | Reliable special bulk |
| **Speed** | 100 | Fast pack-hunter speed tier |

> **Gen 3 Mechanics Note:** In Generation 3, all Dark-type attacks (*Bite*, *Crunch*, *Faint Attack*) are Special, making Fina's 110 Sp. Atk hit hard. Her 80 Attack provides solid utility for physical Normal and Ghost moves like *Return* and *Shadow Ball*.

---

## 3. Level-Up Learnset

| Level | Move | Type | Category (Gen 3) | Power | Acc | PP | Notes |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **1** | Tackle | Normal | Physical | 35 | 95% | 35 | Basic puppy tackle |
| **1** | Tail Whip | Normal | Status | — | 100% | 30 | Lowers target Defense |
| **5** | Charm | Normal | Status | — | 100% | 20 | Sharply lowers target Attack |
| **9** | Quick Attack | Normal | Physical | 40 | 100% | 30 | Priority (+1) |
| **14** | Bite | Dark | Special | 60 | 100% | 25 | STAB on Fina; 30% Flinch |
| **19** | Roar | Normal | Status | — | 100% | 20 | Forces wild flee / switch |
| **24** | Take Down | Normal | Physical | 90 | 85% | 20 | High-power recoil move |
| **29** | Faint Attack | Dark | Special | 60 | — | 20 | STAB; never misses |
| **35** | Crunch | Dark | Special | 80 | 100% | 15 | STAB; 20% lower target Sp. Def |
| **42** | Confuse Ray | Ghost | Status | — | 100% | 10 | 100% accurate confusion |
| **52** | Moonlight | Normal | Status | — | — | 5 | Restores 50% max HP |

---

## 4. TM & HM Compatibility

Both Finita and Fina are compatible with the following Generation 3 TMs and HMs:

| Disc | Move | Type | Cat. (Gen 3) | Power | Acc | PP | Notes |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TM04** | Calm Mind | Psychic | Status | — | — | 20 | Boosts Sp. Atk and Sp. Def |
| **TM06** | Toxic | Poison | Status | — | 85% | 10 | Badly poisons target |
| **TM10** | Hidden Power | Normal | Varies | — | 100% | 15 | Type/power depends on IVs |
| **TM12** | Taunt | Dark | Status | — | 100% | 20 | Prevents status moves |
| **TM15** | Hyper Beam | Normal | Physical | 150 | 90% | 5 | Requires recharge turn |
| **TM17** | Protect | Normal | Status | — | — | 10 | Prevents moves this turn |
| **TM21** | Frustration | Normal | Physical | — | 100% | 20 | Max power at low friendship |
| **TM23** | Iron Tail | Steel | Physical | 100 | 75% | 15 | 30% lower target Defense |
| **TM27** | Return | Normal | Physical | — | 100% | 20 | Signature bond move (102 BP at max friendship) |
| **TM29** | Psychic | Psychic | Special | 90 | 100% | 10 | 10% lower target Sp. Def; counters Fighting weakness |
| **TM30** | Shadow Ball | Ghost | Physical | 80 | 100% | 15 | 20% lower target Sp. Def; Physical in Gen 3 |
| **TM32** | Double Team | Normal | Status | — | — | 15 | Raises evasiveness |
| **TM34** | Shock Wave | Electric | Special | 60 | — | 20 | Never misses |
| **TM40** | Aerial Ace | Flying | Physical | 60 | — | 20 | Never misses |
| **TM41** | Torment | Dark | Status | — | 100% | 15 | Prevents using same move consecutively |
| **TM42** | Facade | Normal | Physical | 70 | 100% | 20 | Doubles power if Burned/Paralyzed/Poisoned |
| **TM43** | Secret Power | Normal | Physical | 70 | 100% | 20 | Secondary effect depends on terrain |
| **TM44** | Rest | Psychic | Status | — | — | 10 | Full recovery, sleeps 2 turns |
| **TM45** | Attract | Normal | Status | — | 100% | 15 | Infatuates opposite gender (stacks with Cute Charm) |
| **TM46** | Thief | Dark | Special | 40 | 100% | 10 | Steals wild/trainer held items |
| **TM49** | Snatch | Dark | Status | — | — | 10 | Steals opponent buff/healing move |
| **HM01** | Cut | Normal | Physical | 50 | 95% | 30 | Field utility |
| **HM04** | Strength | Normal | Physical | 80 | 100% | 15 | Field utility |
| **HM05** | Flash | Normal | Status | — | 70% | 20 | Lowers accuracy; illuminates dark caves |