# Pokémon FireRed: Fina Edition

*FireRed: Fina Edition* is a personalized ROM hack of *Pokémon FireRed* (USA v1.0 / `BPRE0.gba`) created as a gift for my brother. It brings his real Dalmatian dog, **Finita**, and her shadow-guardian evolution, **Fina**, into the Pokémon world as his starting partner.

---

## Story & Concept

Instead of choosing one of the standard Kanto starters, this hack lets the player start their journey with Finita in Pallet Town.

* **Finita (The Spot Pup):** A spirited Normal-type Dalmatian puppy who follows her trainer from the very beginning. She starts off with early-game stats (BST 300) and playful moves.
* **Fina (The Shadow Guardian):** As her bond with her trainer grows, Finita matures into Fina upon leveling up with high friendship (`Friendship >= 220`). Fina is a Dark-type powerhouse (BST 550) with high Special Attack, sleek midnight paw socks, and a protective shadow aura.

---

## Project Structure & Documentation

Detailed design documents, specifications, and scripts are stored in the repository:

* **[`docs/pokemon-fina.md`](file:///home/fernando/workspace/firered/firered-fina/docs/pokemon-fina.md):** Complete breakdown of base stats, abilities, level-up move learnsets, and TM/HM compatibilities.
* **[`docs/sprites.md`](file:///home/fernando/workspace/firered/firered-fina/docs/sprites.md):** Technical sprite standards, 16-color palette index rules, and asset file details.
* **[`patches/hma_finita_fina.txt`](file:///home/fernando/workspace/firered/firered-fina/patches/hma_finita_fina.txt):** Ready-to-import Hex Maniac Advance script for stats, learnsets, evolutions, and text.
* **[`scripts/process_sprites.py`](file:///home/fernando/workspace/firered/firered-fina/scripts/process_sprites.py):** Python pipeline used to convert photo references into GBA-compliant indexed PNG sprites.

---

## Game Sprites & Assets

All battle sprites and party icons follow Generation 3 GBA requirements (64x64 pixels for battle sprites, 32x32 for icons, 16 indexed colors with color 0 transparent keying):

* **Finita Assets:**
  * Front battle sprite: `assets/sprites/finita_front.png`
  * Back battle sprite: `assets/sprites/finita_back.png`
  * Shiny palette variant: `assets/sprites/finita_shiny.png`
  * Party icon: `assets/icons/finita_icon.png`

* **Fina Assets:**
  * Front battle sprite: `assets/sprites/fina_front.png`
  * Back battle sprite: `assets/sprites/fina_back.png`
  * Shiny palette variant: `assets/sprites/fina_shiny.png`
  * Party icon: `assets/icons/fina_icon.png`

---

## How to Build & Patch

1. Open your *Pokémon FireRed* (v1.0 USA / `BPRE`) ROM in **Hex Maniac Advance (HMA)**.
2. Apply the table script from `patches/hma_finita_fina.txt` to set species data.
3. Import the front, back, shiny, and party icon PNGs from `assets/sprites/` and `assets/icons/`.
4. In Oak's Lab (Pallet Town), assign the starter Pokéball gift parameter to `SPECIES_FINITA`.
5. Export the patched ROM and generate a `.bps` delta patch with **Flips** for distribution.

---

## Repository Guidelines

* ROM files (`.gba`) and private reference photos are excluded via `.gitignore` and should never be committed.
* Distribute builds using `.bps` patches.
