import discord.commands
from discord.ext import commands
from constants import BOT_DATA
import database

def is_tathya(ctx):
    return ctx.author.id == 843391557168267295

class AdminCommands(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS)
    @commands.check(is_tathya)
    async def sql(self, ctx, query: str, values: discord.commands.Option(str, "values", required=False)): # type: ignore
        values = values or tuple()
        await ctx.respond(database.run_sql(query, values))
    
def setup(client):
    client.add_cog(AdminCommands(client))
