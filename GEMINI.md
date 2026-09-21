# Project: FireRed Fina Edition

## Objective
A custom ROM hack of *Pokémon FireRed* (v1.0 / USA / `BPRE0.gba`) created as a personal gift for my brother, bringing his real Dalmatian dog, **Finita**, and her shadow-guardian evolution, **Fina**, into the game as his starting companion.

## Overview
* **Finita (Base Form):** The Spot Pup Pokémon. A Normal-type early-game companion (BST ~300) replacing a starter slot in Pallet Town.
* **Fina (Evolved Form):** The Shadow Hound Pokémon. A Dark-type guardian (BST ~550) that evolves when her friendship with her trainer reaches high levels (`Friendship >= 220`).
* **Design & Learnset Details:** See [`docs/pokemon-fina.md`](file:///home/fernando/workspace/firered/firered-fina/docs/pokemon-fina.md).
* **Sprite Specs & Catalog:** See [`docs/sprites.md`](file:///home/fernando/workspace/firered/firered-fina/docs/sprites.md).

## Technical Guidelines
* **ROM Base:** Pokémon FireRed (USA, v1.0) / `BPRE0.gba`.
* **Gen 3 Mechanics:** Standard Generation 3 typing engine (17 original types). Dark attacks are Special; Normal attacks are Physical.
* **Sprite Formatting:**
  * Battle Sprites (Front & Back): 64x64 pixels, 16-color indexed palette.
  * Transparency: Color index `0` is strictly transparent background.
  * Party Icons: 32x32 pixels, 16-color indexed palette.
* **Repository Safety:**
  * Do not commit `.gba` ROM files or private reference photos in Git.
  * Distribute builds using `.bps` delta patches.

## Workflow & Tools
* **Sprite Editing:** Aseprite / GIMP / Python Pillow scripts.
* **ROM Editing:** Hex Maniac Advance (HMA).
* **Patching & Testing:** Flips (`.bps` format) and mGBA emulator.