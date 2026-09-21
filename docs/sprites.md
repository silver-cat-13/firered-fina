# Sprite Artwork & Asset Guide

This document covers all the battle sprites, shiny color palettes, and party icons created for **Finita** and **Fina** in *Pokémon FireRed*.

---

## GBA Sprite Standards

To display correctly in FireRed without graphical glitches or color distortion, all artwork follows strict Generation 3 standards:

* **Battle Sprites (Front, Back & Shiny):** 64 x 64 pixels, 16-color indexed palette (4-bit depth).
* **Party Icons:** 32 x 32 pixels, 16-color indexed palette.
* **Transparent Background Rule:** Color index `0` in the palette is reserved strictly for transparent backgrounds (keyed to green `#00FF00` during processing).
* **Character Colors:** Indexes `1` through `15` are used for body highlights, fur shading, spot outlines, and shadow details.

---

## Asset Files Location

All game-ready PNG assets are organized in the `assets/` folder:

### Finita (Base Puppy Form)
* **Front Sprite:** [`assets/sprites/finita_front.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/finita_front.png) — Playful puppy pose featuring her real-life eye spot patch, chest spots, and floppy ears.
* **Back Sprite:** [`assets/sprites/finita_back.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/finita_back.png) — Over-the-shoulder battle view.
* **Shiny Variant:** [`assets/sprites/finita_shiny.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/finita_shiny.png) — Features midnight violet spots.
* **Party Icon:** [`assets/icons/finita_icon.png`](file:///home/fernando/workspace/firered/firered-fina/assets/icons/finita_icon.png) — 32x32 icon for the party menu and Pokédex.

### Fina (Adult Shadow Guardian)
* **Front Sprite:** [`assets/sprites/fina_front.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/fina_front.png) — Adult Dalmatian hound with midnight paw socks, dark slate ears, glowing amber eyes, and shadow wisps.
* **Back Sprite:** [`assets/sprites/fina_back.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/fina_back.png) — Battle back view showing her shadow aura.
* **Shiny Variant:** [`assets/sprites/fina_shiny.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/fina_shiny.png) — Features deep cobalt blue spots and a glowing aura.
* **Party Icon:** [`assets/icons/fina_icon.png`](file:///home/fernando/workspace/firered/firered-fina/assets/icons/fina_icon.png) — 32x32 icon for the party menu and Pokédex.

---

## How Sprites Were Made

The sprites were processed using Python ([`scripts/process_sprites.py`](file:///home/fernando/workspace/firered/firered-fina/scripts/process_sprites.py)) starting from real-life photos of Fina:

1. **Photo References:** Real photos placed in `pics/` (kept private and excluded via `.gitignore`).
2. **Quantization:** Color depth reduced to 16 colors while preserving spot details and shading.
3. **Palette Alignment:** Background mapped to palette index `0` for clean transparency.
4. **HMA Ready:** Ready to import directly into Hex Maniac Advance without manual indexing fixes.
