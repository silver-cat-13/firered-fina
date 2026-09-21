# Project: FireRed Fina Edition

## Objective
ROM hack of Pokémon FireRed (v1.0 / USA / BPRE) creating a personalized gift for my brother featuring his Dalmatian dog, Finita, and her shadow-guardian evolution, Fina.

## Target Pokémon Specifications
- **Base Form:** Finita (The Spot Pup Pokémon)
  - Type: Normal
  - Abilities: Cute Charm
  - Base Stat Total (BST): ~300
  - Role: Early-game companion / starter replacement
- **Evolved Form:** Fina (The Shadow Hound Pokémon)
  - Type: Dark
  - Abilities: Cute Charm
  - Base Stat Total (BST): ~550
  - Evolution Trigger: High Friendship (`Friendship >= 220`) + Level Up
- **Detailed Design & Learnsets:** Refer to `docs/pokemon-fina.md`

## Technical Constraints & Gen 3 Standards
- **ROM Base:** Pokémon FireRed (USA, v1.0) / `BPRE0.gba`.
- **Typing Engine:** Strict Generation 3 mechanics (17 original types only, no Fairy type).
  - Dark-type attacks are Special.
  - Normal-type attacks are Physical.
- **Sprites:**
  - Dimensions: Exactly 64x64 pixels for Front and Back battle sprites.
  - Color Depth: Indexed 16 colors (4-bit depth).
  - Palette Rule: Color index 0 is strictly transparent background. The remaining 15 colors are for body, shading, and accents.
  - Party Icons: 32x32 pixels, 16-color indexed palette.
- **Repository Safety:**
  - NEVER commit or track `.gba` ROM files in Git.
  - All public distributions must use delta patches (`.bps`).

## Preferred Tools & Workflow
- **Sprite Art:** Aseprite / GIMP (indexed color mode)
- **ROM Editing:** Hex Maniac Advance (HMA)
- **Patching & Testing:** Flips / Romhack.me (`.bps` format) + mGBA emulator