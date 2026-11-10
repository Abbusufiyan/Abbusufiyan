"""
Prepare the portrait photo for clean ASCII conversion:
  1. crop square around the head and shoulders
  2. remove / isolate background onto pure white (255)
  3. enhance linework and facial feature contrast
  4. output: source-prepped.png (grayscale), consumed by make_ascii_svg.py.

Usage:
    python scripts/prep_photo.py [input.png] [output.png]
"""
import os
import sys
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

try:
    import cv2
    import numpy as np
    HAVE_CV2 = True
except ImportError:
    HAVE_CV2 = False


def prep_image(inp_path, out_path):
    im = Image.open(inp_path).convert("RGBA")
    w, h = im.size

    # Target square centered around head/torso (center ~ 527, 450)
    side = min(w, h, 920)
    cx, cy = int(w * 0.49), int(h * 0.35)
    x0 = cx - side // 2
    y0 = cy - side // 2

    canvas = Image.new("RGB", (side, side), (255, 255, 255))
    crop_x0, crop_y0 = max(0, x0), max(0, y0)
    crop_x1, crop_y1 = min(w, x0 + side), min(h, y0 + side)

    sub = im.crop((crop_x0, crop_y0, crop_x1, crop_y1))
    paste_x = crop_x0 - x0
    paste_y = crop_y0 - y0

    # Paste with alpha mask if present
    if sub.mode == "RGBA":
        canvas.paste(sub.convert("RGB"), (paste_x, paste_y), mask=sub.split()[-1])
    else:
        canvas.paste(sub, (paste_x, paste_y))

    # Grayscale
    gray = canvas.convert("L")
    pixels = gray.load()
    rgb_pix = canvas.load()

    # Clear light studio background to pure white (255)
    for y in range(side):
        for x in range(side):
            r, g, b = rgb_pix[x, y]
            if r > 210 and g > 210 and b > 210 and max(abs(r-g), abs(g-b), abs(b-r)) < 20:
                pixels[x, y] = 255

    # Unsharp mask to emphasize edges & facial details
    gray = gray.filter(ImageFilter.UnsharpMask(radius=2.5, percent=160, threshold=2))
    gray = ImageEnhance.Contrast(gray).enhance(1.15)

    gray.save(out_path)
    print(f"wrote {out_path} ({gray.size[0]}x{gray.size[1]})")


if __name__ == "__main__":
    prep_image(INP, OUT)
