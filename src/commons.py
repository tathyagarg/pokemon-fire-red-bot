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
    def __init__(self, query: str, action: typing.Callable) -> None:
        self.query: str = query
        self.action: typing.Callable = action

class Character:
    def __init__(self, name: str, img: str) -> None:
        self.name: str = name
        self.img: str = img
