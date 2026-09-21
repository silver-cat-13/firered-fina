import os
from PIL import Image, ImageOps

def process_to_gba_sprite(input_path, output_path, target_size=(64, 64), max_colors=16):
    img = Image.open(input_path).convert('RGB')
    
    # Resize to target 64x64 using high quality resampling
    img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
    
    # Quantize to 15 colors (+1 for background transparent color)
    # We first make the outer background pure white (255, 255, 255) or magic green (0, 255, 0)
    # Let's inspect top-left corner color as background reference
    bg_ref = img_resized.getpixel((0, 0))
    
    # Map pixels close to background color to pure green (0, 255, 0) for transparent index 0
    data = list(img_resized.getdata())
    new_data = []
    threshold = 35
    for r, g, b in data:
        if abs(r - bg_ref[0]) < threshold and abs(g - bg_ref[1]) < threshold and abs(b - bg_ref[2]) < threshold:
            new_data.append((0, 255, 0)) # Green key
        else:
            new_data.append((r, g, b))
            
    img_keyed = Image.new('RGB', target_size)
    img_keyed.putdata(new_data)
    
    # Quantize to max_colors (16 colors)
    quantized = img_keyed.quantize(colors=max_colors, method=Image.Quantize.MEDIANCUT)
    
    # Ensure color index 0 is the green background (0, 255, 0)
    palette = quantized.getpalette() # list of 768 ints
    # Find which palette index holds (0, 255, 0)
    bg_index = 0
    for i in range(0, max_colors * 3, 3):
        if palette[i] == 0 and palette[i+1] == 255 and palette[i+2] == 0:
            bg_index = i // 3
            break
            
    # Swap index 0 with bg_index if not already 0
    if bg_index != 0:
        pixels = list(quantized.getdata())
        swapped_pixels = []
        for p in pixels:
            if p == 0:
                swapped_pixels.append(bg_index)
            elif p == bg_index:
                swapped_pixels.append(0)
            else:
                swapped_pixels.append(p)
                
        # Swap colors in palette
        c0 = palette[0:3]
        cbg = palette[bg_index*3 : bg_index*3+3]
        palette[0:3] = cbg
        palette[bg_index*3 : bg_index*3+3] = c0
        
        quantized.putdata(swapped_pixels)
        quantized.putpalette(palette)
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    quantized.save(output_path)
    print(f"Saved GBA sprite: {output_path} (Size: {target_size}, Palette: {max_colors} colors)")

def generate_back_sprite(front_path, back_output_path):
    img = Image.open(front_path)
    # Mirror horizontally for back sprite alignment baseline
    back = ImageOps.mirror(img)
    back.save(back_output_path)
    print(f"Saved back sprite baseline: {back_output_path}")

def generate_icon(front_path, icon_output_path):
    process_to_gba_sprite(front_path, icon_output_path, target_size=(32, 32), max_colors=16)

def generate_shiny_palette(sprite_path, shiny_output_path):
    img = Image.open(sprite_path).convert('P')
    palette = img.getpalette()
    
    # Create shiny palette (replace dark spot accents with royal blue/golden glow)
    shiny_palette = palette.copy()
    for i in range(3, 48, 3): # skip index 0
        r, g, b = shiny_palette[i], shiny_palette[i+1], shiny_palette[i+2]
        # Shift dark colors (spots/socks) towards dark cobalt/violet
        if r < 80 and g < 80 and b < 80 and not (r==0 and g==255 and b==0):
            shiny_palette[i] = int(r * 0.5)
            shiny_palette[i+1] = int(g * 0.5 + 40)
            shiny_palette[i+2] = int(b * 0.8 + 120)
            
    img_shiny = img.copy()
    img_shiny.putpalette(shiny_palette)
    img_shiny.save(shiny_output_path)
    print(f"Saved shiny sprite: {shiny_output_path}")

if __name__ == "__main__":
    brain_dir = "/home/fernando/.gemini/antigravity-cli/brain/1e186741-0b45-41e1-bbdd-2154c0ecc658"
    finita_raw = f"{brain_dir}/finita_real_front_1789953986339.jpg"
    fina_raw = f"{brain_dir}/fina_real_front_1789953999004.jpg"
    
    process_to_gba_sprite(finita_raw, "assets/sprites/finita_front.png")
    generate_back_sprite("assets/sprites/finita_front.png", "assets/sprites/finita_back.png")
    generate_icon(finita_raw, "assets/icons/finita_icon.png")
    generate_shiny_palette("assets/sprites/finita_front.png", "assets/sprites/finita_shiny.png")
    
    process_to_gba_sprite(fina_raw, "assets/sprites/fina_front.png")
    generate_back_sprite("assets/sprites/fina_front.png", "assets/sprites/fina_back.png")
    generate_icon(fina_raw, "assets/icons/fina_icon.png")
    generate_shiny_palette("assets/sprites/fina_front.png", "assets/sprites/fina_shiny.png")
