import os
from PIL import Image

# FireRed BPRE v1.0 Sprite & Icon Table Offsets
OFFSET_FRONT_SPRITE_TABLE   = 0x2350AC # Pointer (4 bytes) + Size (4 bytes) per species
OFFSET_FRONT_PALETTE_TABLE  = 0x23730C # Pointer (4 bytes) + Tag (4 bytes) per species
OFFSET_BACK_SPRITE_TABLE    = 0x23654C # Pointer (4 bytes) + Size (4 bytes) per species
OFFSET_BACK_PALETTE_TABLE   = 0x237B0C # Pointer (4 bytes) + Tag (4 bytes) per species
OFFSET_ICON_SPRITE_TABLE    = 0x3D37A0 # Pointer (4 bytes) per species (ucs4x4x8 uncompressed tiles)
OFFSET_ICON_PALETTE_TABLE   = 0x3D3E80 # 1 byte per species (Palette Index 0, 1, or 2)

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

def build_icon_tiles(png_path):
    img = Image.open(png_path).convert('RGB').resize((32, 32), Image.Resampling.LANCZOS)
    pixels = list(img.getdata())
    
    # Map pixels to FireRed Icon Palette 1:
    # 0 = transparent (Green key)
    # 3 = white fur (248, 248, 248)
    # 15 = dark spots / eyes (64, 64, 64)
    # 1 = gray outline (112, 112, 112)
    # 7 = pink tongue (232, 112, 152)
    indices = []
    for r, g, b in pixels:
        if r < 50 and g > 200 and b < 50: # green background key
            indices.append(0)
        elif r > 200 and g < 150 and b < 180: # pink
            indices.append(7)
        elif r < 70 and g < 70 and b < 70: # dark spots / eyes
            indices.append(15)
        elif r < 160 and g < 160 and b < 160: # gray outlines / shading
            indices.append(1)
        else: # white body fur
            indices.append(3)
            
    # GBA 4-bit tile ordering (4 tiles wide x 4 tiles high)
    w, h = 32, 32
    frame = bytearray()
    for tile_y in range(0, h, 8):
        for tile_x in range(0, w, 8):
            for y in range(8):
                for x in range(0, 8, 2):
                    p1 = indices[(tile_y + y) * w + (tile_x + x)] & 0x0F
                    p2 = indices[(tile_y + y) * w + (tile_x + x + 1)] & 0x0F
                    frame.append(p1 | (p2 << 4))
                    
    # Two 32x32 frames required for Gen 3 icons (1024 bytes total)
    return bytes(frame + frame)

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
    
    species_data = [
        (1, "assets/sprites/finita_front.png", "assets/sprites/finita_back.png", "assets/icons/finita_icon.png", 0x1001),
        (2, "assets/sprites/fina_front.png", "assets/sprites/fina_back.png", "assets/icons/fina_icon.png", 0x1002)
    ]
    
    for species_id, front_png, back_png, icon_png, pal_tag in species_data:
        print(f"Applying battle sprites and party icon for species {species_id}...")
        
        # 1. Front Battle Sprite & Palette
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

        # 3. Party Icon Sprite (Two 32x32 uncompressed frames = 1024 bytes)
        icon_tiles = build_icon_tiles(icon_png)
        icon_addr = free_space
        rom[icon_addr : icon_addr + len(icon_tiles)] = icon_tiles
        free_space += len(icon_tiles)
        while free_space % 4 != 0: free_space += 1
        
        # 4. Update Sprite Pointers in ROM tables
        rom[OFFSET_FRONT_SPRITE_TABLE + species_id * 8 : OFFSET_FRONT_SPRITE_TABLE + species_id * 8 + 4] = (front_addr + 0x08000000).to_bytes(4, 'little')
        
        rom[OFFSET_FRONT_PALETTE_TABLE + species_id * 8 : OFFSET_FRONT_PALETTE_TABLE + species_id * 8 + 4] = (front_pal_addr + 0x08000000).to_bytes(4, 'little')
        rom[OFFSET_FRONT_PALETTE_TABLE + species_id * 8 + 4 : OFFSET_FRONT_PALETTE_TABLE + species_id * 8 + 8] = pal_tag.to_bytes(2, 'little') + b'\x00\x00'
        
        rom[OFFSET_BACK_SPRITE_TABLE + species_id * 8 : OFFSET_BACK_SPRITE_TABLE + species_id * 8 + 4] = (back_addr + 0x08000000).to_bytes(4, 'little')
        
        rom[OFFSET_BACK_PALETTE_TABLE + species_id * 8 : OFFSET_BACK_PALETTE_TABLE + species_id * 8 + 4] = (back_pal_addr + 0x08000000).to_bytes(4, 'little')
        rom[OFFSET_BACK_PALETTE_TABLE + species_id * 8 + 4 : OFFSET_BACK_PALETTE_TABLE + species_id * 8 + 8] = pal_tag.to_bytes(2, 'little') + b'\x00\x00'

        # 5. Update Party Icon Pointer & Palette Tables
        rom[OFFSET_ICON_SPRITE_TABLE + species_id * 4 : OFFSET_ICON_SPRITE_TABLE + species_id * 4 + 4] = (icon_addr + 0x08000000).to_bytes(4, 'little')
        rom[OFFSET_ICON_PALETTE_TABLE + species_id] = 1 # Use Palette 1 (white body, black spots)
        
    with open(rom_path, 'wb') as f:
        f.write(rom)
        
    print(f"Successfully inserted battle sprites, palettes, and party icons into {rom_path}!")

if __name__ == "__main__":
    rom_file = "roms/Pokemon_FireRed_Fina_Edition.gba"
    apply_sprites_to_rom(rom_file)
