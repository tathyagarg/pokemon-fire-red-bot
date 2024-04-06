import typing
import discord
from global_vars import *
from database import run_sql
from constants import BOT_DATA

def check_registered(ctx: CTX) -> bool:
    result: list = run_sql("SELECT * FROM {} WHERE {} = ?".format(BOT_DATA.DATABASE.DB_NAME, BOT_DATA.DATABASE.USER_ID), (ctx.author.id,))
    return result != []

def check_registered_without_context(user: discord.User) -> bool:
    result: list = run_sql("SELECT * FROM {} WHERE {} = ?".format(BOT_DATA.DATABASE.DB_NAME, BOT_DATA.DATABASE.USER_ID), (user.id,))
    return result != []

class Input:
    def __init__(self, query: str, action: typing.Callable) -> None:
        self.query: str = query
        self.action: typing.Callable = action

class Character:
    def __init__(self, name: str, img: str) -> None:
        self.name: str = name
        self.img: str = img
