import typing
import discord
import database
from global_vars import *
from constants import BOT_DATA

def check_registered(ctx: CTX) -> bool:
    return database.check_user_exists(uid=ctx.author.id)

def check_registered_without_context(user: discord.User) -> bool:
    return database.check_user_exists(uid=user.id)

class Input:
    def __init__(self, query: str, action: typing.Callable, _filter: typing.Callable = None, placeholder: str = None) -> None:
        self.query = query
        self.action = action
        self._filter = _filter or (lambda v: v)
        self.placeholder = placeholder or ''

class Character:
    def __init__(self, name: str, img: str) -> None:
        self.name = name
        self.img = img

dialogue_default_embed = discord.Embed(
    title='Press >',
    description='Start the dialogue!',
    color=BOT_DATA.COLORS.COLOR_PRIMARY
)
