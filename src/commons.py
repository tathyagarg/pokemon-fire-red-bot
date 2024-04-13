import enum
import typing
import discord
import database
from global_vars import *
from constants import BOT_DATA

def check_registered(ctx: CTX) -> bool:
    return database.check_user_exists(uid=ctx.author.id)

def check_registered_without_context(user: discord.User) -> bool:
    return database.check_user_exists(uid=user.id)

class Direction(enum.Enum):
    BACK = 0
    RIGHT = 1
    FRONT = 2
    LEFT = 3
    BACK_RIGHT = 4
    BACK_LEFT = 5
    UP_RIGHT = 6
    UP_LEFT = 7

    @classmethod
    def fetch(cls, idx: int) -> enum.Enum:
        return cls._value2member_map_[idx]

class Input:
    def __init__(self, query: str, action: typing.Callable, _filter: typing.Callable = None, placeholder: str = None) -> None:
        self.query = query
        self.action = action
        self._filter = _filter or (lambda v: v)
        self.placeholder = placeholder or ''

class OverworldSprites:
    def __init__(self, front: str, right: str, back: str, left: str) -> None:
        self.front = front
        self.right = right
        self.back = back
        self.left = left

        self.sprites = [
            self.back,
            self.right,
            self.front,
            self.left
        ]

    def from_direction(self, direction: Direction) -> str:
        return self.sprites[direction.value]

class Character:
    def __init__(self, name: str, img: str, overworld_sprites: OverworldSprites = None) -> None:
        self.name = name
        self.img = img
        self.overworld_sprites = overworld_sprites

dialogue_default_embed = discord.Embed(
    title='Press >',
    description='Start the dialogue!',
    color=BOT_DATA.COLORS.COLOR_PRIMARY
)
