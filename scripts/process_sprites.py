import os
from PIL import Image, ImageOps

def process_gba_sprite_clean(input_path, output_path, target_size=(64, 64)):
    img = Image.open(input_path).convert('RGB')
    img = img.resize(target_size, Image.Resampling.LANCZOS)
    
    # 1. Flood fill or detect background color from top-left pixel (0,0)
    bg_ref = img.getpixel((0, 0))
    
    # We will map outer background to pure magenta (255, 0, 255)
    # Inner white/light pixels will be adjusted to (248, 248, 248) so they never match magenta background
    pixels = list(img.getdata())
    new_pixels = []
    
    # BFS / Flood fill from outer edges to mark background pixels
    w, h = target_size
    is_bg = [[False]*w for _ in range(h)]
    queue = [(0, 0), (w-1, 0), (0, h-1), (w-1, h-1)]
    for x, y in queue:
        is_bg[y][x] = True
        
    threshold = 45
    while queue:
        cx, cy = queue.pop(0)
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h and not is_bg[ny][nx]:
                r, g, b = pixels[ny * w + nx]
                if abs(r - bg_ref[0]) < threshold and abs(g - bg_ref[1]) < threshold and abs(b - bg_ref[2]) < threshold:
                    is_bg[ny][nx] = True
                    queue.append((nx, ny))
                    
    for y in range(h):
        for x in range(w):
            idx = y * w + x
            if is_bg[y][x]:
                new_pixels.append((0, 255, 0)) # Green key for background index 0
            else:
                r, g, b = pixels[idx]
                # If body pixel is pure green or close to green key, shift it slightly so it doesn't key out
                if r < 30 and g > 220 and b < 30:
                    g = 200
                new_pixels.append((r, g, b))
                
    img_keyed = Image.new('RGB', target_size)
    img_keyed.putdata(new_pixels)
    
    # Quantize to 16 colors
    quantized = img_keyed.quantize(colors=16, method=Image.Quantize.MEDIANCUT)
    
    # Ensure Index 0 is background green (0, 255, 0)
    palette = quantized.getpalette()
    bg_index = 0
    for i in range(0, 48, 3):
        if palette[i] == 0 and palette[i+1] == 255 and palette[i+2] == 0:
            bg_index = i // 3
            break
            
    if bg_index != 0:
        pix = list(quantized.getdata())
        swapped = []
        for p in pix:
            if p == 0: swapped.append(bg_index)
            elif p == bg_index: swapped.append(0)
            else: swapped.append(p)
            
        c0 = palette[0:3]
        cbg = palette[bg_index*3 : bg_index*3+3]
        palette[0:3] = cbg
        palette[bg_index*3 : bg_index*3+3] = c0
        
        quantized.putdata(swapped)
        quantized.putpalette(palette)
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    quantized.save(output_path)
    print(f"Processed clean GBA sprite: {output_path}")

def generate_back_sprite(front_path, back_output_path):
    img = Image.open(front_path)
    back = ImageOps.mirror(img)
    back.save(back_output_path)

def generate_icon(front_path, icon_output_path):
    process_gba_sprite_clean(front_path, icon_output_path, target_size=(32, 32))

def generate_shiny(sprite_path, shiny_output_path):
    img = Image.open(sprite_path).convert('P')
    palette = img.getpalette()
    shiny_palette = palette.copy()
    for i in range(3, 48, 3):
        r, g, b = shiny_palette[i], shiny_palette[i+1], shiny_palette[i+2]
        if r < 80 and g < 80 and b < 80 and not (r==0 and g==255 and b==0):
            shiny_palette[i] = int(r * 0.5)
            shiny_palette[i+1] = int(g * 0.5 + 40)
            shiny_palette[i+2] = int(b * 0.8 + 120)
    img_shiny = img.copy()
    img_shiny.putpalette(shiny_palette)
    img_shiny.save(shiny_output_path)

if __name__ == "__main__":
    brain_dir = "/home/fernando/.gemini/antigravity-cli/brain/1e186741-0b45-41e1-bbdd-2154c0ecc658"
    finita_raw = f"{brain_dir}/finita_real_front_1789953986339.jpg"
    fina_raw = f"{brain_dir}/fina_real_front_1789953999004.jpg"
    
    process_gba_sprite_clean(finita_raw, "assets/sprites/finita_front.png")
    generate_back_sprite("assets/sprites/finita_front.png", "assets/sprites/finita_back.png")
    generate_icon(finita_raw, "assets/icons/finita_icon.png")
    generate_shiny("assets/sprites/finita_front.png", "assets/sprites/finita_shiny.png")
    
    process_gba_sprite_clean(fina_raw, "assets/sprites/fina_front.png")
    generate_back_sprite("assets/sprites/fina_front.png", "assets/sprites/fina_back.png")
    generate_icon(fina_raw, "assets/icons/fina_icon.png")
    generate_shiny("assets/sprites/fina_front.png", "assets/sprites/fina_shiny.png")
