import pathlib
import os
from PIL import Image

def resize_images(assets_path: str = None, starting_idx: int = 0, size: tuple[int, int] = None):
    size = size or (128, 128)
    here = pathlib.Path(__file__).parent.parent.joinpath(assets_path or 'assets')
    for file in os.listdir(here):
        if file.endswith('.png'):
            idx = int(file[:3])
            if idx < starting_idx:
                continue

            with Image.open(here.joinpath(file)) as img:
                img = img.resize(size)
                img.save(here.joinpath(file))
                print(f"Altered {file}")

def main():
    while True:
        action = input(">>> ").lower()
        if action == "resize":
            print("Resizing images...")
            resize_images()
        elif action in ("quit", "exit"):
            print("Exiting.")
            break
        else:
            print("Unrecognized action")

if __name__ == "__main__":
    main()
