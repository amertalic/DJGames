import os
from PIL import Image

# Define the directory
IMAGE_DIR = "/home/amer/Desktop/Projects/DJGames/src/static/images"
QUALITY = 80  # Adjust quality (80 is a good balance between size and quality)

# Supported image formats
EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")


def compress_image(image_path):
    try:
        with Image.open(image_path) as img:
            img_format = img.format  # Preserve original format
            img = (
                img.convert("RGB") if img_format in ["JPEG", "JPG"] else img
            )  # Ensure RGB mode

            # Save compressed image (overwrite the original)
            img.save(image_path, format=img_format, quality=QUALITY, optimize=True)
            print(f"Compressed: {image_path}")

    except Exception as e:
        print(f"Failed to process {image_path}: {e}")


def process_images(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(EXTENSIONS):
                image_path = os.path.join(root, file)
                compress_image(image_path)


if __name__ == "__main__":
    process_images(IMAGE_DIR)
    print("✅ Image compression completed!")
