import os
import discord
import pathlib
from constants import BOT_DATA
from discord.ext import commands

def load_cogs(client):
    cogs_dir = pathlib.Path(__file__).parent.joinpath('cogs')
    for cog in os.listdir(cogs_dir):
        if cog.endswith('.py'):
            client.load_extension(f"cogs.{cog[:-3]}")
            print(f"Loaded cogs/{cog}")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is ready to go!")

load_cogs(bot)
bot.run(BOT_DATA.TOKEN)
