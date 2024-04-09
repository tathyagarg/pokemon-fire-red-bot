import os
import console
import pathlib
import database
from PIL import Image
from global_vars import *

def error_suppress(func):
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(f'Encountered error: {e}')
    
    return inner

def int_validate(message: str, acceptable_range: range = None) -> int:
    while True:
        try:
            result = int(console.input(message=message))
            if acceptable_range:
                assert result-1 in acceptable_range
            return result
        except ValueError:
            print('Invalid.')
        except AssertionError:
            print('Too high/low')

class Utils:
    def __init__(self, bot: BOT) -> None:
        self.bot = bot

    def resize_images(self, assets_path: str, starting_idx: int = 0, size: tuple[int, int] = None) -> None:
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

    def resize_one(self, assets_path: str, size_multiplier: int = 2) -> None:
        here: pathlib.PosixPath = pathlib.Path(__file__).parent.parent.joinpath(assets_path)
        with Image.open(fp=here) as img:
            img: Image = img.resize((img.size[0] * size_multiplier, img.size[1] * size_multiplier))
            img.save(fp=here)
            print(f"Altered {assets_path}")

    @error_suppress
    def load_cog(self) -> None:
        extension: str = console.input('Extension>>> ')
        self.bot.load_extension(extension)

    @error_suppress
    def unload_cog(self) -> None:
        extension: str = console.input('Extension>>> ')
        self.bot.unload_extension(extension)

    @error_suppress
    def reload_cog(self) -> None:
        extension: str = console.input('Extension>>> ')
        self.bot.unload_extension(extension)
        self.bot.load_extension(extension)

    def list_cogs(self) -> None:
        for i, ext in enumerate(self.bot.extensions, 1):
            print(f"[{i}] {ext}")

    def run(self):
        frame = console.Frame(rows=10)
        frame.register_text('Shell Admin Interface')

        frame.display()

        options = {
            'Load Cog': self.load_cog,
            'Unload Cog': self.unload_cog,
            'Reload Cog': self.reload_cog,
            'List cogs': self.list_cogs,
            'Flush': lambda: -1,
            'Kill': 1,
        }

        print(console.COLORS.INFO)
        for i, option in enumerate(options, 1):
            print(f"[{i}] {option}")

        while True:
            choice = int_validate('>>> ', range(len(options)))-1
            option = list(options)[choice]
            if option == 'Kill':
                break
            options[list(options)[choice]]()

        return 0
