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

    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS)
    @commands.check(is_tathya)
    async def clear_table(self, ctx, new_table: discord.commands.Option(str, "new_table_query", required=False)): # type: ignore
        database.run_sql('DROP TABLE Users')
        if new_table:
            database.run_sql('CREATE TABLE {}'.format(new_table))
        
        await ctx.respond("Done!")

def setup(client):
    client.add_cog(AdminCommands(client))
