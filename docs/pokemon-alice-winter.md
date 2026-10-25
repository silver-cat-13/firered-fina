# Alice & Winter: Pokémon Design, Lore & Stats

This document details the complete design, lore, battle statistics, learnsets, and sprite specifications for **Alice** and **Winter**, replacing Zapdos and Articuno in *Pokémon FireRed*.

---

## Concept & Lore

### 1. Alice (The Curious Spark Pokémon)
* **Real-Life Inspiration:** Alice is an energetic, wildly curious tabby girl cat with distinctive brown/grey tabby stripes, white muzzle and chest bib, curious green eyes, white mittens/socks, and an unquenchable drive to explore.
* **Role & Lore:** 
  * Alice is captivated by human ingenuity, mechanisms, and inventions. She wandered into Kanto's abandoned **Power Plant** (replacing Zapdos) not out of territorial aggression, but to curiously investigate and play with the generators, coils, and electrical machinery.
  * She has a deep love for potatoes and will run around at blinding speed playing with coils and toys.
  * When encountered in the Power Plant, her playful static electricity sparks across the machines as she greets the trainer with an inquisitive meow.
* **Typing:** Mono Electric (`ELECTRIC / ELECTRIC`)
* **Ability:** **Speed Boost** — Reflects her boundless energy and high-speed playful dashes around the house.
* **Base Stat Total:** 580 (Legendary BST)
  * Focus: Extreme Speed & Special Attack; lowest stat is HP.

---

### 2. Winter (The Dormant Shadow Pokémon)
* **Real-Life Inspiration:** Winter is a fluffy, gentle black-and-white boy cat with a black "mask/cap" over his head, a white blaze down his face, a signature black dot on his pink nose, and a deeply peaceful demeanor.
* **Role & Lore:**
  * In contrast to Alice's hyperactive curiosity, Winter is dormant, quiet, shy, and loves to sleep for hours curled on his back.
  * He secluded himself deep within the icy caverns of the **Seafoam Islands** (replacing Articuno) to escape noise and human contact. 
  * Despite his solitary nature, Winter possesses immense affection for every living creature. He harbors zero malice and radiates a gentle, warm presence through the shadows.
  * Most importantly, Winter shares an unbreakable, timeless bond with Alice—even though they dwell on opposite sides of Kanto in the game, their spirits resonate across the region.
* **Typing:** Mono Ghost (`GHOST / GHOST`)
* **Ability:** **Shadow Tag** — His shadowy embrace prevents foes from escaping his soothing presence.
* **Base Stat Total:** 580 (Legendary BST)
  * Focus: Heavy Physical Attack & Sturdy Defense; lowest stat is Speed (sleepy and dormant).

---

## Base Stats & Battle Roles

### Alice (Electric)
* **Battle Role:** Lightning-fast Special sweeper with snowballing Speed Boost.
* **EV Yield:** +3 Speed (or +2 Speed, +1 Sp. Atk)
* **Catch Rate:** 3 (Legendary) / Base Exp: 216 / Gender: 100% Female (`254`)

| Stat | Value | Strategic Role |
| :--- | :---: | :--- |
| **HP** | 65 | Lowest stat; nimble glass-cannon profile |
| **Attack** | 70 | Secondary physical cat claw/slash utility |
| **Defense** | 75 | Decent physical defense to take priority hits |
| **Sp. Atk** | 140 | Massive electrical special power (Thunderbolt/Thunder) |
| **Sp. Def** | 80 | Reliable special bulk against beam attacks |
| **Speed** | 150 | Top-tier speed, further amplified by Speed Boost |
| **BST** | **580** | Matches Legendary Bird benchmark |

---

### Winter (Ghost)
* **Battle Role:** Bulky physical Ghost tank and trapper with Shadow Tag and devastating STAB Shadow Ball.
* **EV Yield:** +2 Defense, +1 Attack
* **Catch Rate:** 3 (Legendary) / Base Exp: 216 / Gender: 100% Male (`0`)

| Stat | Value | Strategic Role |
| :--- | :---: | :--- |
| **HP** | 110 | Fluffy, massive health pool |
| **Attack** | 130 | Heavy physical paw strikes (Gen 3 Ghost moves are Physical!) |
| **Defense** | 135 | Impenetrable physical bulk |
| **Sp. Atk** | 65 | Modest special output |
| **Sp. Def** | 90 | Solid special resistance |
| **Speed** | 50 | Lowest stat; sleepy, dormant, unhurried |
| **BST** | **580** | Matches Legendary Bird benchmark |

> **Gen 3 Battle Note:** In Generation 3, Ghost attacks (*Shadow Ball*, *Shadow Punch*, *Astonish*) calculate damage using the Pokémon's **Physical Attack stat**. This makes Winter's 130 Attack an absolute powerhouse with STAB *Shadow Ball*, while Alice's 140 Special Attack maximizes Electric moves (*Thunderbolt*, *Shock Wave*, *Thunder*).

---

## Level-Up Learnsets

### Alice (Curious Electric Cat)
| Level | Move | Type | Category (Gen 3) | Power | Acc | PP | Flavor / Notes |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **1** | Quick Attack | Normal | Physical | 40 | 100% | 30 | Playful feline pounce (Priority +1) |
| **1** | ThunderShock | Electric | Special | 40 | 100% | 30 | Initial static spark |
| **5** | Fake Out | Normal | Physical | 40 | 100% | 10 | Playful cat surprise (100% flinch on Turn 1) |
| **12** | Charge | Electric | Status | — | — | 20 | Powers up next electric attack, raises SpD |
| **18** | Spark | Electric | Special | 65 | 100% | 20 | Electric tackle (30% paralysis) |
| **25** | Screech | Normal | Status | — | 85% | 40 | Cat screech, sharply lowers foe Defense |
| **32** | Shock Wave | Electric | Special | 60 | — | 20 | Swift never-miss electric discharge |
| **39** | Slash | Normal | Physical | 70 | 100% | 20 | Sharp feline claw slash (High crit) |
| **45** | Thunderbolt | Electric | Special | 95 | 100% | 15 | Signature high-power STAB |
| **52** | Agility | Psychic | Status | — | — | 30 | Lightning zoomies (+2 Speed) |
| **59** | Thunder | Electric | Special | 120 | 70% | 10 | Cataclysmic storm discharge |
| **66** | Zap Cannon | Electric | Special | 100 | 50% | 5 | Massive blast from human inventions (100% paralyze) |

### Winter (Dormant Ghost Cat)
| Level | Move | Type | Category (Gen 3) | Power | Acc | PP | Flavor / Notes |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **1** | Astonish | Ghost | Physical | 30 | 100% | 15 | Gentle ghostly surprise (30% flinch) |
| **1** | Lick | Ghost | Physical | 20 | 100% | 30 | Affectionate cat lick (30% paralysis) |
| **5** | Yawn | Normal | Status | — | 100% | 10 | Contagious sleepiness (Puts foe to sleep next turn) |
| **12** | Night Shade | Ghost | Special | Level | 100% | 15 | Whispering shadows dealing fixed damage |
| **18** | Confuse Ray | Ghost | Status | — | 100% | 10 | Gentle dancing ghostly lights |
| **25** | Curse | Ghost | Status | — | — | 10 | Ghostly sacrifice binding target |
| **32** | Shadow Punch | Ghost | Physical | 60 | — | 20 | Never-miss shadowy paw swipe |
| **39** | Rest | Psychic | Status | — | — | 10 | Dormant sleep, fully restores HP & cures status |
| **45** | Snore | Normal | Special | 40 | 100% | 15 | Loud sleepy snores while asleep (30% flinch) |
| **52** | Shadow Ball | Ghost | Physical | 80 | 100% | 15 | Devastating physical STAB (20% SpD drop) |
| **59** | Body Slam | Normal | Physical | 85 | 100% | 15 | Hefty fluffy pounce (30% paralysis) |
| **66** | Destiny Bond | Ghost | Status | — | — | 5 | Eternal bond, takes attacker down with him |

---

## TM & HM Compatibility

### Alice
* **STAB & Special Coverage:** TM24 (Thunderbolt), TM25 (Thunder), TM34 (Shock Wave), TM29 (Psychic), TM30 (Shadow Ball).
* **Setup & Utility:** TM04 (Calm Mind), TM06 (Toxic), TM10 (Hidden Power), TM12 (Taunt), TM15 (Hyper Beam), TM16 (Light Screen), TM17 (Protect), TM18 (Rain Dance), TM21 (Frustration), TM23 (Iron Tail), TM27 (Return), TM28 (Dig), TM32 (Double Team), TM33 (Reflect), TM40 (Aerial Ace), TM41 (Torment), TM42 (Facade), TM43 (Secret Power), TM44 (Rest), TM45 (Attract), TM46 (Thief).
* **Field HMs:** HM01 (Cut), HM04 (Strength), HM05 (Flash), HM06 (Rock Smash).

### Winter
* **STAB & Physical Coverage:** TM30 (Shadow Ball), TM26 (Earthquake), TM31 (Brick Break), TM36 (Sludge Bomb), TM23 (Iron Tail), TM28 (Dig), TM27 (Return), TM21 (Frustration).
* **Setup & Sleep Utility:** TM04 (Calm Mind), TM06 (Toxic), TM10 (Hidden Power), TM12 (Taunt), TM15 (Hyper Beam), TM17 (Protect), TM18 (Rain Dance), TM20 (Safeguard), TM29 (Psychic), TM32 (Double Team), TM41 (Torment), TM42 (Facade), TM43 (Secret Power), TM44 (Rest), TM45 (Attract), TM46 (Thief), TM49 (Snatch).
* **Field HMs:** HM01 (Cut), HM04 (Strength), HM05 (Flash), HM06 (Rock Smash).

---

## Pokédex Data & In-Game Encounter

### Alice (Species 145 / Power Plant)
* **Category:** `"CURIOUS CAT"`
* **Height:** `0.4 m` ($4$ dm)
* **Weight:** `4.2 kg` ($42$ hg)
* **Pokédex Description:**
  ```text
  A playful, curious cat who loves\n
  potatoes. Drawn to inventions, she\n
  shares a special bond with WINTER.
  ```
* **Encounter Cry:** Meowth playful meow (DirectSound Cry `51`).
* **Encounter Text:** Replaces Zapdos's generic "Gyaoo!" with:
  `"Nyaa-zap! Alice playfully darts\naround the generator machinery!\p"`

### Winter (Species 144 / Seafoam Islands)
* **Category:** `"DORMANT CAT"`
* **Height:** `0.5 m` ($5$ dm)
* **Weight:** `5.5 kg` ($55$ hg)
* **Pokédex Description:**
  ```text
  A shy, sleepy cat resting in caves\n
  to find peace. Loving to all life,\n
  he shares a warm bond with ALICE.
  ```
* **Encounter Cry:** Persian gentle purr/meow (DirectSound Cry `52`).
* **Encounter Text:** Replaces Articuno's generic "Gyaoo!" with:
  `"Mroww... Winter peeks from the shadows,\nsoftly purring with quiet warmth.\p"`

---

## Overworld Sprites (In-Game Field)

Both Alice and Winter feature customized $32 \times 32$ overworld sprites for their stationary map encounters:
* **Alice:** Replaces Zapdos overworld sprite (`GFX 136`) in Power Plant. Sitting alert, upright, with white chest and curious green eyes.
* **Winter:** Replaces Articuno overworld sprite (`GFX 138`) in Seafoam Islands B4F. Fluffy, loafing or curled peacefully in the ice cavern.
