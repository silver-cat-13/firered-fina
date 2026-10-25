import os
import struct
from PIL import Image

# FireRed BPRE v1.0 Sprite & Icon Table Offsets
OFFSET_FRONT_SPRITE_TABLE    = 0x2350AC # Pointer (4 bytes) + Size (4 bytes) per species
OFFSET_FRONT_PALETTE_TABLE   = 0x23730C # Pointer (4 bytes) + Tag (4 bytes) per species
OFFSET_BACK_SPRITE_TABLE     = 0x23654C # Pointer (4 bytes) + Size (4 bytes) per species
OFFSET_BACK_PALETTE_TABLE    = 0x237B0C # Pointer (4 bytes) + Tag (4 bytes) per species
OFFSET_FRONT_SHINY_PAL_TABLE = 0x2380CC # Pointer (4 bytes) + Tag (4 bytes) per species
OFFSET_BACK_SHINY_PAL_TABLE  = 0x2388CC # Pointer (4 bytes) + Tag (4 bytes) per species
OFFSET_ICON_SPRITE_TABLE     = 0x3D37A0 # Pointer (4 bytes) per species (ucs4x4x8 uncompressed tiles)
OFFSET_ICON_PALETTE_TABLE    = 0x3D3E80 # 1 byte per species (Palette Index 0, 1, or 2)

# Overworld Sprite & Palette Tables
OFFSET_OW_PALETTE_TABLE      = 0x3A5158 # Array of [pal_ptr (4), tag (2), pad (2)]
OFFSET_ZAPDOS_OW_IMAGES      = 0x3A2290 # GFX 136 SpriteFrameImage array (10 frames x 8 bytes)
OFFSET_ARTICUNO_OW_IMAGES    = 0x3A2320 # GFX 138 SpriteFrameImage array (10 frames x 8 bytes)

def color_to_rgb555(r, g, b):
    r5 = (r >> 3) & 0x1F
    g5 = (g >> 3) & 0x1F
    b5 = (b >> 3) & 0x1F
    val = r5 | (g5 << 5) | (b5 << 10)
    return val.to_bytes(2, 'little')

def png_to_gba_tiles(png_path, target_size=(64, 64)):
    img = Image.open(png_path).convert('P')
    w, h = img.size
    palette = img.getpalette()
    
    gba_palette = bytearray()
    for i in range(16):
        r, g, b = palette[i*3], palette[i*3+1], palette[i*3+2]
        gba_palette.extend(color_to_rgb555(r, g, b))
        
    raw_pixels = list(img.getdata())
    gba_tiles = bytearray()
    
    for tile_y in range(0, h, 8):
        for tile_x in range(0, w, 8):
            for y in range(8):
                for x in range(0, 8, 2):
                    px1 = raw_pixels[(tile_y + y) * w + (tile_x + x)] & 0x0F
                    px2 = raw_pixels[(tile_y + y) * w + (tile_x + x + 1)] & 0x0F
                    byte_val = px1 | (px2 << 4)
                    gba_tiles.append(byte_val)
                    
    return bytes(gba_tiles), bytes(gba_palette)

def ow_png_to_tiles_and_pal(png_path):
    img = Image.open(png_path).convert('P')
    w, h = img.size
    palette = img.getpalette()
    
    gba_palette = bytearray()
    for i in range(16):
        r, g, b = palette[i*3], palette[i*3+1], palette[i*3+2]
        gba_palette.extend(color_to_rgb555(r, g, b))
        
    raw_pixels = list(img.getdata())
    tiles = bytearray()
    for ty in range(0, h, 8):
        for tx in range(0, w, 8):
            for y in range(8):
                for x in range(0, 8, 2):
                    p1 = raw_pixels[(ty + y)*w + (tx + x)] & 0x0F
                    p2 = raw_pixels[(ty + y)*w + (tx + x + 1)] & 0x0F
                    tiles.append(p1 | (p2 << 4))
    return bytes(tiles), bytes(gba_palette)

def build_icon_tiles(png_path):
    img = Image.open(png_path)
    w, h = img.size
    
    frames = []
    if h >= 64:
        frames.append(img.crop((0, 0, 32, 32)))
        frames.append(img.crop((0, 32, 32, 64)))
    else:
        f0 = img.crop((0, 0, 32, 32))
        frames.append(f0)
        f1 = Image.new(f0.mode, (32, 32), 0 if f0.mode == 'P' else (0, 255, 0))
        if f0.mode == 'P':
            f1.putpalette(f0.getpalette())
        f1.paste(f0.crop((0, 0, 32, 31)), (0, 1))
        frames.append(f1)
        
    tiles_total = bytearray()
    for frame_img in frames:
        if frame_img.mode == 'P':
            pixels = list(frame_img.getdata())
        else:
            rgb_pixels = list(frame_img.convert('RGB').getdata())
            pixels = []
            for r, g, b in rgb_pixels:
                if r < 50 and g > 200 and b < 50:
                    pixels.append(0)
                elif r > 200 and g < 150 and b < 180:
                    pixels.append(7)
                elif r < 70 and g < 70 and b < 70:
                    pixels.append(15)
                elif r < 120 and g < 120 and b < 120:
                    pixels.append(14)
                elif r < 160 and g < 160 and b < 160:
                    pixels.append(1)
                elif r < 210 and g < 210 and b < 210:
                    pixels.append(2)
                else:
                    pixels.append(3)
                    
        # GBA 4-bit tile ordering (4 tiles wide x 4 tiles high)
        frame_bytes = bytearray()
        for tile_y in range(0, 32, 8):
            for tile_x in range(0, 32, 8):
                for y in range(8):
                    for x in range(0, 8, 2):
                        p1 = pixels[(tile_y + y) * 32 + (tile_x + x)] & 0x0F
                        p2 = pixels[(tile_y + y) * 32 + (tile_x + x + 1)] & 0x0F
                        frame_bytes.append(p1 | (p2 << 4))
        tiles_total.extend(frame_bytes)
        
    return bytes(tiles_total)

def lz77_compress(data):
    uncompressed_len = len(data)
    out = bytearray()
    out.append(0x10)
    out.extend((uncompressed_len).to_bytes(3, 'little'))
    
    pos = 0
    while pos < uncompressed_len:
        flag_pos = len(out)
        out.append(0)
        flag_byte = 0
        
        for bit in range(8):
            if pos >= uncompressed_len:
                break
                
            best_len = 0
            best_disp = 0
            max_search = min(pos, 4096)
            
            for disp in range(1, max_search + 1):
                length = 0
                while (pos + length < uncompressed_len and 
                       length < 18 and 
                       data[pos + length] == data[pos - disp + length]):
                    length += 1
                if length > best_len:
                    best_len = length
                    best_disp = disp
                    if length == 18:
                        break
                        
            if best_len >= 3:
                flag_byte |= (1 << (7 - bit))
                len_bits = (best_len - 3) & 0x0F
                disp_bits = (best_disp - 1) & 0x0FFF
                val = (len_bits << 12) | disp_bits
                out.extend(val.to_bytes(2, 'big'))
                pos += best_len
            else:
                out.append(data[pos])
                pos += 1
                
        out[flag_pos] = flag_byte
        
    return bytes(out)

def apply_sprites_to_rom(rom_path):
    with open(rom_path, 'rb') as f:
        rom = bytearray(f.read())
        
    free_space = 0xE3C000
    
    # Species Data: (ID, front_png, back_png, shiny_png, icon_png, pal_tag, icon_palette_index)
    species_data = [
        (1, "assets/sprites/finita_front.png", "assets/sprites/finita_back.png", "assets/sprites/finita_shiny.png", "assets/icons/finita_icon.png", 0x1001, 1),
        (2, "assets/sprites/fina_front.png", "assets/sprites/fina_back.png", "assets/sprites/fina_shiny.png", "assets/icons/fina_icon.png", 0x1002, 1),
        (144, "assets/sprites/winter_front.png", "assets/sprites/winter_back.png", "assets/sprites/winter_shiny.png", "assets/icons/winter_icon.png", 0x1003, 0),
        (145, "assets/sprites/alice_front.png", "assets/sprites/alice_back.png", "assets/sprites/alice_shiny.png", "assets/icons/alice_icon.png", 0x1004, 0)
    ]
    
    for species_id, front_png, back_png, shiny_png, icon_png, pal_tag, icon_pal in species_data:
        print(f"Applying battle sprites and party icon for species {species_id}...")
        
        # 1. Front Battle Sprite & Normal Palette
        front_tiles, front_pal = png_to_gba_tiles(front_png, target_size=(64, 64))
        compressed_front = lz77_compress(front_tiles)
        compressed_front_pal = lz77_compress(front_pal)
        
        front_addr = free_space
        rom[front_addr : front_addr + len(compressed_front)] = compressed_front
        free_space += len(compressed_front)
        while free_space % 4 != 0: free_space += 1
        
        front_pal_addr = free_space
        rom[front_pal_addr : front_pal_addr + len(compressed_front_pal)] = compressed_front_pal
        free_space += len(compressed_front_pal)
        while free_space % 4 != 0: free_space += 1
        
        # 2. Back Battle Sprite & Palette
        back_tiles, back_pal = png_to_gba_tiles(back_png, target_size=(64, 64))
        compressed_back = lz77_compress(back_tiles)
        compressed_back_pal = lz77_compress(back_pal)
        
        back_addr = free_space
        rom[back_addr : back_addr + len(compressed_back)] = compressed_back
        free_space += len(compressed_back)
        while free_space % 4 != 0: free_space += 1
        
        back_pal_addr = free_space
        rom[back_pal_addr : back_pal_addr + len(compressed_back_pal)] = compressed_back_pal
        free_space += len(compressed_back_pal)
        while free_space % 4 != 0: free_space += 1

        # 3. Shiny Palette (Front & Back)
        if shiny_png and os.path.exists(shiny_png):
            _, shiny_pal = png_to_gba_tiles(shiny_png, target_size=(64, 64))
            compressed_shiny_pal = lz77_compress(shiny_pal)
            shiny_pal_addr = free_space
            rom[shiny_pal_addr : shiny_pal_addr + len(compressed_shiny_pal)] = compressed_shiny_pal
            free_space += len(compressed_shiny_pal)
            while free_space % 4 != 0: free_space += 1
            
            # Update Front & Back Shiny Palette Tables
            rom[OFFSET_FRONT_SHINY_PAL_TABLE + species_id * 8 : OFFSET_FRONT_SHINY_PAL_TABLE + species_id * 8 + 4] = (shiny_pal_addr + 0x08000000).to_bytes(4, 'little')
            rom[OFFSET_FRONT_SHINY_PAL_TABLE + species_id * 8 + 4 : OFFSET_FRONT_SHINY_PAL_TABLE + species_id * 8 + 8] = (pal_tag + 0x100).to_bytes(2, 'little') + b'\x00\x00'
            
            rom[OFFSET_BACK_SHINY_PAL_TABLE + species_id * 8 : OFFSET_BACK_SHINY_PAL_TABLE + species_id * 8 + 4] = (shiny_pal_addr + 0x08000000).to_bytes(4, 'little')
            rom[OFFSET_BACK_SHINY_PAL_TABLE + species_id * 8 + 4 : OFFSET_BACK_SHINY_PAL_TABLE + species_id * 8 + 8] = (pal_tag + 0x100).to_bytes(2, 'little') + b'\x00\x00'

        # 4. Party Icon Sprite (Two 32x32 uncompressed frames = 1024 bytes)
        icon_tiles = build_icon_tiles(icon_png)
        icon_addr = free_space
        rom[icon_addr : icon_addr + len(icon_tiles)] = icon_tiles
        free_space += len(icon_tiles)
        while free_space % 4 != 0: free_space += 1
        
        # 5. Update Battle Sprite Pointers in ROM tables
        rom[OFFSET_FRONT_SPRITE_TABLE + species_id * 8 : OFFSET_FRONT_SPRITE_TABLE + species_id * 8 + 4] = (front_addr + 0x08000000).to_bytes(4, 'little')
        rom[OFFSET_FRONT_PALETTE_TABLE + species_id * 8 : OFFSET_FRONT_PALETTE_TABLE + species_id * 8 + 4] = (front_pal_addr + 0x08000000).to_bytes(4, 'little')
        rom[OFFSET_FRONT_PALETTE_TABLE + species_id * 8 + 4 : OFFSET_FRONT_PALETTE_TABLE + species_id * 8 + 8] = pal_tag.to_bytes(2, 'little') + b'\x00\x00'
        
        rom[OFFSET_BACK_SPRITE_TABLE + species_id * 8 : OFFSET_BACK_SPRITE_TABLE + species_id * 8 + 4] = (back_addr + 0x08000000).to_bytes(4, 'little')
        rom[OFFSET_BACK_PALETTE_TABLE + species_id * 8 : OFFSET_BACK_PALETTE_TABLE + species_id * 8 + 4] = (back_pal_addr + 0x08000000).to_bytes(4, 'little')
        rom[OFFSET_BACK_PALETTE_TABLE + species_id * 8 + 4 : OFFSET_BACK_PALETTE_TABLE + species_id * 8 + 8] = pal_tag.to_bytes(2, 'little') + b'\x00\x00'

        # 6. Update Party Icon Pointer & Palette Tables
        rom[OFFSET_ICON_SPRITE_TABLE + species_id * 4 : OFFSET_ICON_SPRITE_TABLE + species_id * 4 + 4] = (icon_addr + 0x08000000).to_bytes(4, 'little')
        rom[OFFSET_ICON_PALETTE_TABLE + species_id] = icon_pal

    # 7. Overworld Stationary Sprites (Alice -> Power Plant, Winter -> Seafoam Islands)
    ow_data = [
        # (name, png_path, images_table_offset, pal_table_index)
        ("Alice", "assets/sprites/alice_overworld.png", OFFSET_ZAPDOS_OW_IMAGES, 0),    # Zapdos slot, Tag 0x1103
        ("Winter", "assets/sprites/winter_overworld.png", OFFSET_ARTICUNO_OW_IMAGES, 1) # Articuno slot, Tag 0x1104
    ]

    for name, png_path, images_offset, pal_idx in ow_data:
        if os.path.exists(png_path):
            print(f"Applying overworld stationary sprite for {name}...")
            ow_tiles, ow_pal = ow_png_to_tiles_and_pal(png_path)
            
            ow_tiles_addr = free_space
            rom[ow_tiles_addr : ow_tiles_addr + len(ow_tiles)] = ow_tiles
            free_space += len(ow_tiles)
            while free_space % 4 != 0: free_space += 1
            
            ow_pal_addr = free_space
            rom[ow_pal_addr : ow_pal_addr + len(ow_pal)] = ow_pal
            free_space += len(ow_pal)
            while free_space % 4 != 0: free_space += 1
            
            # Point all 10 frames in SpriteFrameImage table to the new 32x32 tiles
            for frame_idx in range(10):
                entry_addr = images_offset + frame_idx * 8
                rom[entry_addr : entry_addr + 4] = (ow_tiles_addr + 0x08000000).to_bytes(4, 'little')
                rom[entry_addr + 4 : entry_addr + 6] = (512).to_bytes(2, 'little')
                
            # Point entry in graphics.overworld.palettes (0x3A5158 + pal_idx * 8) to new palette
            pal_entry_addr = OFFSET_OW_PALETTE_TABLE + pal_idx * 8
            rom[pal_entry_addr : pal_entry_addr + 4] = (ow_pal_addr + 0x08000000).to_bytes(4, 'little')

    with open(rom_path, 'wb') as f:
        f.write(rom)
        
    print(f"Successfully inserted battle sprites, palettes, party icons, and overworld sprites into {rom_path}!")

if __name__ == "__main__":
    rom_file = "roms/Pokemon_FireRed_Fina_Edition.gba"
    apply_sprites_to_rom(rom_file)
