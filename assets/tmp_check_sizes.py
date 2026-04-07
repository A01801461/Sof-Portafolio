import os
from PIL import Image

def get_sizes(directory):
    for root, d, files in os.walk(directory):
        for file in files:
            if file.endswith('.webp'):
                path = os.path.join(root, file)
                with Image.open(path) as img:
                    print(f"{path}: {img.size}")
                break # print just one per folder
                
if __name__ == "__main__":
    print("HIGH:")
    get_sizes("assets/img/high/photography")
    print("STD:")
    get_sizes("assets/img/std/photography")
