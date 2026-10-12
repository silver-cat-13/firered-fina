# Next Steps & Handoff Guide: FireRed Fina Edition

**Date:** October 12, 2026  
**Target ROM:** Pokémon FireRed (USA v1.0 / `BPRE0.gba`)  
**Output ROM:** [`roms/Pokemon_FireRed_Fina_Edition.gba`](file:///home/fernando/workspace/firered/firered-fina/roms/Pokemon_FireRed_Fina_Edition.gba)

---

## 1. Work Completed in This Session

### A. Finita (Species #1 — Base Puppy Form)
* **Front Battle Sprite ([`assets/sprites/finita_front.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/finita_front.png)):** Replaced the cropped puppy bust with a full-body alert seated quadruped pose inspired by Vulpix. All four paws are now visible and grounded on screen, with her signature left-eye Dalmatian patch and floppy ears.
* **Back Battle Sprite ([`assets/sprites/finita_back.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/finita_back.png)):** Replaced the horizontally mirrored front sprite with an authentic Gen 3 over-the-shoulder rear perspective facing the battlefield.
* **Shiny Variant ([`assets/sprites/finita_shiny.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/finita_shiny.png)):** Re-indexed to 16 colors with midnight violet spots.

### B. Fina (Species #2 — Adult Shadow Guardian Evolution)
* **Front Battle Sprite ([`assets/sprites/fina_front.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/fina_front.png)):**
  * Eliminated the duplicate floating head artifact in the upper-left corner.
  * Replaced high-res downscaled art with authentic Gen 3 pixel art proportions and bold outlines.
  * Floppy white ears covered with black Dalmatian dots (matching Finita).
  * White tail with Dalmatian spots and dark tip.
  * Midnight black shadow socks on all four legs with shadow flame wisps.
* **Back Battle Sprite ([`assets/sprites/fina_back.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/fina_back.png)):**
  * Replaced the mirrored image with a true rear battle perspective looking forward-right toward the opponent.
  * Ears now have Dalmatian spots matching the front sprite and Finita (no longer solid black blocks).
  * Tail is white with Dalmatian spots and a dark tip (matching the front sprite instead of being all black).
  * Feet and shadow socks match the front sprite.
* **Shiny Variant ([`assets/sprites/fina_shiny.png`](file:///home/fernando/workspace/firered/firered-fina/assets/sprites/fina_shiny.png)):** Deep cobalt blue spots, socks, and accents.

### C. Build Pipeline
* Ran [`scripts/patch_rom.py`](file:///home/fernando/workspace/firered/firered-fina/scripts/patch_rom.py), successfully inserting all 6 updated battle sprites into [`roms/Pokemon_FireRed_Fina_Edition.gba`](file:///home/fernando/workspace/firered/firered-fina/roms/Pokemon_FireRed_Fina_Edition.gba).

---

## 2. Priority Issues to Fix Next (For Tomorrow's Agent)

### 🔴 Priority 1: Party Screen Menu Icon ("Pokemon Screen")
* **Problem:** In the in-game Start $\rightarrow$ POKÉMON menu (Party screen), Finita's icon looks distorted, truncated, or misplaced (see [`pics/sprite-issue.png`](file:///home/fernando/workspace/firered/firered-fina/pics/sprite-issue.png) and [`pics/Screenshot from 2026-09-20 22-51-03.png`](file:///home/fernando/workspace/firered/firered-fina/pics/Screenshot%20from%202026-09-20%2022-51-03.png)).
* **Root Causes to Address:**
  1. [`assets/icons/finita_icon.png`](file:///home/fernando/workspace/firered/firered-fina/assets/icons/finita_icon.png) and [`assets/icons/fina_icon.png`](file:///home/fernando/workspace/firered/firered-fina/assets/icons/fina_icon.png) were downscaled from large images and are blurry, taking up only a tiny portion of the 32x32 canvas.
  2. In [`scripts/patch_sprites.py`](file:///home/fernando/workspace/firered/firered-fina/scripts/patch_sprites.py), `build_icon_tiles()` blurs the PNG again with Lanczos and applies lossy RGB thresholding instead of using direct indexed palette indices.
  3. FireRed Party Icon Palette 1 has specific indexed slots:
     * Index `0`: Transparent background
     * Index `1`: Medium gray outline (`#707070`)
     * Index `2`: Light gray shading (`#B8B8B8`)
     * Index `3`: White fur (`#F8F8F8`)
     * Index `7`: Pink tongue/ears (`#E87098`)
     * Index `14`: Dark gray (`#606058`)
     * Index `15`: Black spots/eyes (`#404040`)
* **Action Required:**
  * Design clean, crisp 32x32 pixel-art icons for Finita and Fina centered properly on the canvas with appropriate headroom.
  * Provide two animation frames (Frame 0 and Frame 1, 512 bytes each, 1024 bytes total uncompressed).
  * Direct-index the pixel data into Palette 1 slots.

---

### 🟡 Priority 2: Relative Sprite Scale Polish (Puppy vs Adult)
* **Problem:** Both Finita (puppy) and Fina (adult) currently measure 58 pixels tall inside their 64x64 canvases. Finita's head and body feel almost the same size as adult Fina on screen.
* **Action Required:**
  * Scale Finita slightly down inside her 64x64 canvas (to approx. 44–46 pixels tall with 10–12 pixels headroom/padding).
  * This creates an immediate visual contrast: Finita looks like an adorable, compact puppy, and Fina visibly looms larger upon evolution.

---

### 🟢 Priority 3: Testing Configuration vs Final Release
* **Testing Convenience:**
  * In [`scripts/patch_rom.py`](file:///home/fernando/workspace/firered/firered-fina/scripts/patch_rom.py#L91), Finita's base friendship is currently `70` (standard starter friendship, evolving around Lv 16–20).
  * For fast iteration testing, temporarily set line 91 to `215` so she evolves into Fina immediately on Level 5 $\rightarrow$ Level 6.
  * For the final gift release, ensure base friendship is restored to `70` and canonical stats are preserved.

---

## 3. Toolchain & Quick Commands

* **Rebuild the ROM from scratch:**
  ```bash
  /usr/bin/python3 scripts/patch_rom.py
  ```
* **Verify Sprite Formats:**
  * Resolution: Exactly 64x64 pixels (battle sprites) / 32x32 pixels (icons).
  * Color mode: Indexed 16 colors (4-bit depth).
  * Palette index `0`: `#00FF00` transparent green key.
