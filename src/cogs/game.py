from global_vars import *
from constants import BOT_DATA
from discord.ext import commands
from commons import check_registered

class Game(commands.Cog):
    def __init__(self, bot: BOT) -> None:
        self.bot: BOT = bot

    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS)
    @commands.check(check_registered)
    async def game(self, ctx: CTX) -> None:
        await ctx.respond("WIP")

def setup(client: BOT) -> None:
    client.add_cog(cog=Game(bot=client))
