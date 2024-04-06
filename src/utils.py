import os
import pathlib
from PIL import Image

def resize_images(assets_path: str, starting_idx: int = 0, size: tuple[int, int] = None) -> None:
    size: tuple[int, int] = size or (128, 128)
    here: pathlib.PosixPath = pathlib.Path(__file__).parent.parent.joinpath(assets_path)
    for file in os.listdir(path=here):
        if file.endswith('.png'):
            idx: int = int(file[:3])
            if idx < starting_idx:
                continue

            with Image.open(fp=here.joinpath(file)) as img:
                img: Image = img.resize(size)
                img.save(fp=here.joinpath(file))
                print(f"Altered {file}")

def resize_one(assets_path: str, size_multiplier: int = 2) -> None:
    here: pathlib.PosixPath = pathlib.Path(__file__).parent.parent.joinpath(assets_path)
    with Image.open(fp=here) as img:
        img: Image = img.resize((img.size[0] * size_multiplier, img.size[1] * size_multiplier))
        img.save(fp=here)
        print(f"Altered {assets_path}")

def main() -> None:
    while True:
        action: str = input(">>> ").lower()
        match action.split():
            case ["resize", assets_path, multiplier]:
                print("Resizing image...")
                resize_one(assets_path=assets_path, size_multiplier=int(multiplier))
            case ["resize", assets_path]:
                print("Resizing image...")
                resize_one(assets_path=assets_path)
            case ["resize"]:
                print("Resizing images...")
                resize_images(assets_path='assets/menu_sprites')
            case ["quit"] | ["exit"]:
                print("Exiting.")
                break
            case _:
                print("Unrecognized action")

if __name__ == "__main__":
    main()
