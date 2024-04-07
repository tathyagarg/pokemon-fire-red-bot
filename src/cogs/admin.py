import commons
import discord
import constants
from global_vars import *
from database import run_sql
from constants import BOT_DATA
from extensions import dialogue
from discord.ext import commands
from entities import pokemon, data

DATABASE: constants.Database = BOT_DATA.DATABASE

def is_tathya(ctx: CTX) -> bool:
    return ctx.author.id == 843391557168267295


class AdminCommands(commands.Cog):
    def __init__(self, bot: BOT) -> None:
        self.bot: BOT = bot

    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS, description='Run SQL commands on the users.sql file')
    @commands.check(is_tathya)
    async def sql(self, ctx: CTX, query: str, values: str = "") -> None:
        values: tuple[str, ...] = values or tuple()
        await ctx.respond(run_sql(sql=query, values=values))

    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS, description='Delete all contents of the table, or reinitalize a new table')
    @commands.check(is_tathya)
    async def clear_table(self, ctx: CTX, new_table: str = "") -> None:
        if new_table:
            run_sql(sql='DROP TABLE {}'.format(DATABASE.DB_NAME))
            run_sql(sql='CREATE TABLE {}'.format(new_table))
        else:
            run_sql(sql='DELETE FROM {}'.format(DATABASE.DB_NAME))
        
        await ctx.respond("Done!")

    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS, description='Add a Pokemon from given instance data to the author\'s party')
    @commands.check(is_tathya)
    async def add_pokemon_to_party(self, ctx: CTX, instance_data: str) -> None:
        result: str = run_sql(sql="SELECT {} FROM {} WHERE {}=?".format(DATABASE.PARTY, DATABASE.DB_NAME, DATABASE.USER_ID), values=(ctx.author.id,))[0][0]
        new_party: str = (result + f'.<{instance_data}>').strip('.   ')
        run_sql(sql="UPDATE {} SET {}=? WHERE {}=?".format(DATABASE.DB_NAME, DATABASE.PARTY, DATABASE.USER_ID), values=(new_party, ctx.author.id,))
        await ctx.respond("Updated!")

    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS, description='Create a pokemon with random stats')
    @commands.check(is_tathya)
    async def make_new(self, ctx: CTX, pokedex: int = 1) -> None:
        pkmn: pokemon.PokemonInstance = pokemon.PokemonInstance(parent=pokemon.Pokemon.all_pokemon[pokedex-1])
        await ctx.respond(pkmn.encode())

    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS, description='Test out the newest beta feature')
    @commands.check(is_tathya)
    async def new_feature(self, ctx: CTX) -> None:
        msg: INTERACTION = await ctx.respond('abc')  # TODO: Add a default embed
        d: dialogue.Dialogue = dialogue.Dialogue(
            msg_id=msg.id,
            displays=[
                (data.PROFESSOR_OAK, 'a', None),
                (data.PROFESSOR_OAK, 'b', commons.Input(
                    '???',
                    lambda value: run_sql(
                        sql="UPDATE {} SET {} = ? WHERE {} = ?".format(DATABASE.DB_NAME, DATABASE.USE_NAME, DATABASE.USER_ID),
                        values=(value, ctx.author.id)
                    )
                )),
                (data.PROFESSOR_OAK, 'c', None)
            ]
        )
        await (await msg.original_response()).edit(view=d.paginator)

class CogManager(commands.Cog):
    def __init__(self, bot: BOT) -> None:
        self.bot: BOT = bot

    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS, description='List all active extensions')
    @commands.check(is_tathya)
    async def list_cogs(self, ctx: CTX) -> None:
        description: str = ""
        for i, cog in enumerate(self.bot.extensions, 1):
            description += f"{i}. {cog}\n"

        embed: discord.Embed = discord.Embed(
            color=BOT_DATA.COLORS.COLOR_PRIMARY,
            title="Cogs",
            description=description
        )

        await ctx.respond(embed=embed)

    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS, description='Unload a specific extension')
    @commands.check(is_tathya)
    async def unload_cog(self, ctx: CTX, cog_name: str) -> None:
        cog_name: str = f"cogs.{cog_name}"
        if cog_name not in self.bot.extensions:
            await ctx.respond("Extension not found.")
            return
        
        self.bot.unload_extension(name=cog_name)
        await ctx.respond(f"Unloaded extension {cog_name}")

    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS, description='Load a specific extension')
    @commands.check(is_tathya)
    async def load_cog(self, ctx: CTX, cog_name: str) -> None:
        cog_name: str = f"cogs.{cog_name}"
        
        self.bot.load_extension(name=cog_name)
        await ctx.respond(f"Loaded extension {cog_name}")

    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS, description='Reload a specific extension')
    @commands.check(is_tathya)
    async def reload_cog(self, ctx: CTX, cog_name: str) -> None:
        cog_name: str = f"cogs.{cog_name}"
        if cog_name not in self.bot.extensions:
            await ctx.respond("Extension not found.")
            return 
        
        self.bot.unload_extension(name=cog_name)
        self.bot.load_extension(name=cog_name)
        await ctx.respond(f"Reloaded extension {cog_name}")

def setup(client: BOT) -> None:
    client.add_cog(cog=AdminCommands(bot=client))
    client.add_cog(cog=CogManager(bot=client))
