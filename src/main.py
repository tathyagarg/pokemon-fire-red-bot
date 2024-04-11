import os
import time
import utils
import console
import discord
import pathlib
import argparse
import threading
from global_vars import *
from constants import BOT_DATA
from discord.ext import commands

def load_cogs(client: BOT) -> None:
    cogs_dir: pathlib.PosixPath = pathlib.Path(__file__).parent.joinpath('cogs')

    cogs = [cog for cog in os.listdir(path=cogs_dir) if cog.endswith('.py')]
    info = console.COLORS.INFO

    for cog in cogs:
        if cog.endswith('.py'):
            client.load_extension(name=f"cogs.{cog[:-3]}")
            text = f'[{time.time():.2f}] Loaded cogs/{cog}'
            print(info + text)

intents: discord.Intents = discord.Intents.all()
bot: BOT = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready() -> None:
    print(console.COLORS.INFO + f"[{time.time():.2f}] {bot.user} is ready to go!")

def greet() -> None:
    frame = console.Frame(rows=12)
    frame.register_text('Pokemon Fire Red Bot')
    frame.display()
    print(f"{'By Tathya Garg': ^{os.get_terminal_size().columns}}")
    frame.reset()

def main() -> None:
    print(console.COLORS.INFO + f"[{time.time():.2f}] Launching")

    load_cogs(client=bot)

    bot.run(BOT_DATA.TOKEN)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--without-shell', action='store_const', const=True, default=False)
    without_shell = parser.parse_args().without_shell

    greet()
    if not without_shell:
        threading.Thread(target=main).start()
        utils.Utils(bot=bot).run()
    else:
        main()

