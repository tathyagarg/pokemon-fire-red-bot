import sys
from .colors import COLORS

def input(message: str) -> str:
    print(COLORS.INPUT_PROMPT, message, COLORS.INPUT, sep='')
    result = sys.stdin.readline().strip()
    print(COLORS.RESET, end='')

    return result
