# QuickPic Core CLI Engine
import os
from PIL import Image

def resize_image(image_path, output_path, max_width=1200):
    with Image.open(image_path) as img:
        w_percent = (max_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((max_width, h_size), Image.Resampling.LANCZOS)
        img.save(output_path, "WEBP", quality=85)
        print(f"Processed: {output_path}")

if __name__ == "__main__":
    print("QuickPic CLI Core ready.")
