import os
import discord
import pathlib
from global_vars import *
from constants import BOT_DATA
from discord.ext import commands

def load_cogs(client: BOT) -> None:
    cogs_dir: pathlib.PosixPath = pathlib.Path(__file__).parent.joinpath('cogs')
    for cog in os.listdir(path=cogs_dir):
        if cog.endswith('.py'):
            client.load_extension(name=f"cogs.{cog[:-3]}")
            print(f"Loaded cogs/{cog}")

intents: discord.Intents = discord.Intents.all()
bot: BOT = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready() -> None:
    print(f"{bot.user} is ready to go!")

def main() -> None:
    load_cogs(client=bot)
    bot.run(BOT_DATA.TOKEN)

if __name__ == "__main__":
    main()
