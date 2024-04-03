from discord.ext import commands
from constants import BOT_DATA
from commons import check_registered

class Game(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS)
    @commands.check(check_registered)
    async def game(self, ctx):
        await ctx.respond("WIP")

def setup(client):
    client.add_cog(Game(client))
