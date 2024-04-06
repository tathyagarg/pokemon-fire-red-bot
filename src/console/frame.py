import os
import typing
from constants import BOT_DATA
from .character_data import CHARACTERS, HEIGHT

cases = ['═', '╔', '╗', '╚', '╝', '║']
COLOR_STRING = '\x01\x1b[38;2;{};{};{}m'

def hex_to_rgb(hex: int) -> tuple[int, int, int]:
    blue = hex & 255
    green = (hex >> 8) & 255
    red = (hex >> 16) & 255

    return red, green, blue

class Frame:
    def __init__(self, cols: int = 0, rows: int = 0, color_start: int = BOT_DATA.COLORS.COLOR_PRIMARY, color_end: int = BOT_DATA.COLORS.COLOR_SECONDARY) -> None:
        terminal_size = os.get_terminal_size()

        self.rows = rows or terminal_size.lines
        self.cols = cols or terminal_size.columns

        self.bookings = []
        self.booking_start = -1
        self.booking_end = -1

        self.text_start_y = ((self.rows - HEIGHT - 2) // 2) + 1

        self.color_start = color_start
        self.color_end = color_end

    def display(self) -> None:
        for y, gradient in zip(range(self.rows), generate_gradient(self.rows, self.color_start, self.color_end)):
            for x in range(self.cols):
                print(gradient, end='')
                if x == y == 0: print(cases[1], end='')
                elif x == self.cols-1 and y == 0: print(cases[2], end='')
                elif x == 0 and y == self.rows-1: print(cases[3], end='')
                elif x == self.cols-1 and y == self.rows-1: print(cases[4], end='')
                elif y in (0, self.rows-1): print(cases[0], end='')
                elif x in (0, self.cols-1): print(cases[5], end='')
                elif self.booking_start <= x+1 <= self.booking_end and HEIGHT + self.text_start_y > y >= self.text_start_y:
                    print(self.bookings[y-self.text_start_y][x+1], end='')
                else: print(' ', end='')
            print()

    def register_text(self, text: str) -> None:
        variables: list[str] = []
        for character in text:
            if character.isupper():
                idx: int = ord(character) - 65
                variables.append(CHARACTERS[idx])
            elif character.islower():
                idx: int = ord(character) - 71
                variables.append(CHARACTERS[idx])
            elif character == ' ':
                variables.append(CHARACTERS[-1])

        for i in range(HEIGHT):
            self.bookings.append('')
            for character in variables:
                self.bookings[-1] += character.splitlines()[i]

        for i in range(len(self.bookings)):
            self.bookings[i] = f'{self.bookings[i]: ^{self.cols}}'
        
        widest_idx = max(range(len(self.bookings)), key=lambda i: len(self.bookings[i].strip()))
        self.booking_start = self.bookings[widest_idx].find(self.bookings[widest_idx].strip()[0])
        self.booking_end = self.bookings[widest_idx].rfind(self.bookings[widest_idx].strip()[-1])

    def reset(self) -> None:
        print('\x01\x1b[0m\x02')

def generate_gradient(size: int, color_start: int = BOT_DATA.COLORS.COLOR_PRIMARY, color_end: int = BOT_DATA.COLORS.COLOR_SECONDARY) -> typing.Generator[str, None, None]:
    start = hex_to_rgb(color_start)
    end = hex_to_rgb(color_end)

    red_step: float = (start[0] - end[0]) / size
    green_step: float = (start[1] - end[1]) / size
    blue_step: float = (start[2] - end[2]) / size

    for i in range(size):
        r = int(start[0] - (red_step * i))
        g = int(start[1] - (green_step * i))
        b = int(start[2] - (blue_step * i))

        yield COLOR_STRING.format(r, g, b)

def generate_code(color: int) -> str:
    r, g, b = hex_to_rgb(color)
    return COLOR_STRING.format(r, g, b)

info_color = generate_code(BOT_DATA.COLORS.COLOR_INFO)
