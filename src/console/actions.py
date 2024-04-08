import sys
from .colors import COLORS

def input(message: str) -> str:
    sys.stdout.write(COLORS.INPUT_PROMPT + message + COLORS.INPUT)
    sys.stdout.flush()
    result = sys.stdin.readline().strip()
    print(COLORS.RESET, end='')

    return result
