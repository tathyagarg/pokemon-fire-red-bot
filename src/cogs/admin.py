import discord.commands
from discord.ext import commands
from constants import BOT_DATA
from database import run_sql
from entities import pokemon

def is_tathya(ctx):
    return ctx.author.id == 843391557168267295

class AdminCommands(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS)
    @commands.check(is_tathya)
    async def sql(self, ctx, query: str, values: str = ""):
        values = values or tuple()
        await ctx.respond(run_sql(query, values))

    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS)
    @commands.check(is_tathya)
    async def clear_table(self, ctx, new_table: str = ""):
        if new_table:
            run_sql('DROP TABLE {}'.format(BOT_DATA.DATABASE.DB_NAME))
            run_sql('CREATE TABLE {}'.format(new_table))
        else:
            run_sql('DELETE FROM {}'.format(BOT_DATA.DATABASE.DB_NAME))
        
        await ctx.respond("Done!")

    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS)
    @commands.check(is_tathya)
    async def add_pokemon_to_party(self, ctx, instance_data):
        result = run_sql("SELECT {} FROM {} WHERE {}=?".format(BOT_DATA.DATABASE.PARTY, BOT_DATA.DATABASE.DB_NAME, BOT_DATA.DATABASE.USER_ID), (ctx.author.id,))[0][0]
        new_party = (result + f'.<{instance_data}>').strip('.   ')
        run_sql("UPDATE {} SET {}=? WHERE {}=?".format(BOT_DATA.DATABASE.DB_NAME, BOT_DATA.DATABASE.PARTY, BOT_DATA.DATABASE.USER_ID), (new_party, ctx.author.id,))
        await ctx.respond("Updated!")

    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS)
    @commands.check(is_tathya)
    async def make_new(self, ctx, pokedex: int = 1):
        pkmn = pokemon.PokemonInstance(pokemon.Pokemon.all_pokemon[pokedex-1])
        await ctx.respond(pkmn.encode())        

class CogManager(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS)
    @commands.check(is_tathya)
    async def list_cogs(self, ctx):
        description = ""
        for i, cog in enumerate(self.bot.extensions, 1):
            description += f"{i}. {cog}\n"

        embed = discord.Embed(
            color=BOT_DATA.COLORS.COLOR_PRIMARY,
            title="Cogs",
            description=description
        )

        await ctx.respond(embed=embed)

    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS)
    @commands.check(is_tathya)
    async def unload_cog(self, ctx, cog_name: str):
        cog_name = f"cogs.{cog_name}"
        if cog_name not in self.bot.extensions:
            await ctx.respond("Extension not found.")
            return 
        
        self.bot.unload_extension(cog_name)
        await ctx.respond(f"Unloaded extension {cog_name}")

    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS)
    @commands.check(is_tathya)
    async def load_cog(self, ctx, cog_name: str):
        cog_name = f"cogs.{cog_name}"
        
        self.bot.load_extension(cog_name)
        await ctx.respond(f"Loaded extension {cog_name}")

    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS)
    @commands.check(is_tathya)
    async def reload_cog(self, ctx, cog_name: str):
        cog_name = f"cogs.{cog_name}"
        if cog_name not in self.bot.extensions:
            await ctx.respond("Extension not found.")
            return 
        
        self.bot.unload_extension(cog_name)
        self.bot.load_extension(cog_name)
        await ctx.respond(f"Reloaded extension {cog_name}")

def setup(client):
    client.add_cog(AdminCommands(client))
    client.add_cog(CogManager(client))
