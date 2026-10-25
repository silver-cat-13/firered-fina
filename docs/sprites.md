# Sprite Artwork & Asset Guide

This document covers all the battle sprites, shiny color palettes, party icons, and overworld stationary sprites created for **Finita & Fina** and **Alice & Winter** in *Pokémon FireRed*.

---

## GBA Sprite Standards

To display correctly in FireRed without graphical glitches or color distortion, all artwork follows strict Generation 3 standards:

* **Battle Sprites (Front, Back & Shiny):** 64 x 64 pixels, 16-color indexed palette (4-bit depth, mode `P`).
* **Party Icons:** 32 x 64 pixels (two animated 32x32 frames), 16-color indexed palette.
* **Overworld Sprites:** 32 x 32 pixels, 16-color indexed palette (4-bit depth, mode `P`).
* **Transparent Background Rule:** Color index `0` in the palette is reserved strictly for transparent backgrounds (keyed to green `#00FF00` during processing).
* **Character Colors:** Indexes `1` through `15` are used for highlights, shading, markings, and shadow/spark details.

---

## Asset Files Location

All game-ready PNG assets are organized in the `assets/` folder:

### 1. Finita (Base Puppy Form — Species 1 / Bulbasaur Slot)
* **Front Sprite:** [`assets/sprites/finita_front.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/finita_front.png) — Playful puppy pose featuring her real-life eye spot patch, chest spots, and floppy ears.
* **Back Sprite:** [`assets/sprites/finita_back.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/finita_back.png) — Over-the-shoulder battle view.
* **Shiny Variant:** [`assets/sprites/finita_shiny.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/finita_shiny.png) — Features midnight violet spots.
* **Party Icon:** [`assets/icons/finita_icon.png`](file:///home/fernando/workspace/firered/firered-fina/assets/icons/finita_icon.png) — 32x64 dual-frame animated icon (Palette 1).

### 2. Fina (Adult Shadow Guardian — Species 2 / Ivysaur Slot)
* **Front Sprite:** [`assets/sprites/fina_front.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/fina_front.png) — Adult Dalmatian hound with midnight paw socks, dark slate ears, glowing amber eyes, and shadow wisps.
* **Back Sprite:** [`assets/sprites/fina_back.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/fina_back.png) — Battle back view showing her shadow aura.
* **Shiny Variant:** [`assets/sprites/fina_shiny.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/fina_shiny.png) — Features deep cobalt blue spots and a glowing aura.
* **Party Icon:** [`assets/icons/fina_icon.png`](file:///home/fernando/workspace/firered/firered-fina/assets/icons/fina_icon.png) — 32x64 dual-frame animated icon (Palette 1).

### 3. Alice (The Curious Electric Cat — Species 145 / Zapdos Slot)
* **Front Sprite:** [`assets/sprites/alice_front.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/alice_front.png) — Agile tabby cat with brown/grey stripes, white muzzle and chest bib, curious green eyes, white mittens, and crackling yellow static sparks.
* **Back Sprite:** [`assets/sprites/alice_back.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/alice_back.png) — Over-the-shoulder rear battle perspective with perked ears, ringed tail, and static arcs.
* **Shiny Variant:** [`assets/sprites/alice_shiny.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/alice_shiny.png) — Warm golden amber coat with electric cyan sparks and sapphire eyes.
* **Party Icon:** [`assets/icons/alice_icon.png`](file:///home/fernando/workspace/firered/firered-fina/assets/icons/alice_icon.png) — 32x64 dual-frame animated icon (Palette 0).
* **Overworld Sprite:** [`assets/sprites/alice_overworld.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/alice_overworld.png) — 32x32 stationary overworld NPC sprite in the Power Plant (`GFX 136`).

### 4. Winter (The Dormant Ghost Cat — Species 144 / Articuno Slot)
* **Front Sprite:** [`assets/sprites/winter_front.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/winter_front.png) — Fluffy black-and-white tuxedo cat loafing peacefully, with black cap, white facial blaze, signature black nose dot, big fluffy black tail, and ethereal lavender ghost smoke wisps.
* **Back Sprite:** [`assets/sprites/winter_back.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/winter_back.png) — Rear battle perspective showing his black head cap, fluffy white neck ruff, black back patch, and rising ghost mist.
* **Shiny Variant:** [`assets/sprites/winter_shiny.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/winter_shiny.png) — Obsidian navy sheen with ghostly icy cyan/aqua mist.
* **Party Icon:** [`assets/icons/winter_icon.png`](file:///home/fernando/workspace/firered/firered-fina/assets/icons/winter_icon.png) — 32x64 dual-frame animated icon (Palette 0).
* **Overworld Sprite:** [`assets/sprites/winter_overworld.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/winter_overworld.png) — 32x32 stationary overworld NPC sprite in Seafoam Islands B4F (`GFX 138`).

---

## How Sprites Were Made

The sprites were created and processed starting from real-life reference photos of Alice and Winter in `pics/winter-and-alice`:

1. **Photo Analysis:** Real photos analyzed for exact fur patterns, ear shapes, facial blazes, and distinctive markings (Alice's white socks and blaze; Winter's nose dot and head cap).
2. **Gen 3 Pixel Art Translation:** Scaled to 64x64 and 32x32 pixel art matching canonical Generation 3 Pokémon anatomy, line weight, and dynamic battle poses.
3. **Palette Quantization:** Strictly quantized to 16 colors with background keyed to `#00FF00` at index `0`.
4. **Automated ROM Insertion:** Handled natively by [`scripts/patch_sprites.py`](file:///home/fernando/workspace/firered/firered-fina/scripts/patch_sprites.py) with LZ77 compression and table pointer repointing.
