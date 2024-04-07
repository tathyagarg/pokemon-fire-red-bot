from .frame import generate_code
from constants import BOT_DATA

class COLORS:
    INFO: str = generate_code(BOT_DATA.COLORS.COLOR_INFO)
    INPUT_PROMPT: str = generate_code(0x4ACF3E)
    INPUT: str = generate_code(0x42d7f5)
    RESET: str = '\x01\x1b[0m\x02'
