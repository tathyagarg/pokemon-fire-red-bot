import commons
import discord
import database
import constants
from global_vars import *
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

    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS, description='Add a Pokemon from given instance data to the author\'s party')
    @commands.check(is_tathya)
    async def add_pokemon_to_party(self, ctx: CTX, instance_data: str) -> None:
        database.update_field(
            uid=ctx.author.id,
            field=DATABASE.PARTY,
            new_value=database.request_field(uid=ctx.author.id, field=DATABASE.PARTY) + [instance_data]
        )

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
                    lambda value: database.update_field(
                        uid=ctx.author.id,
                        field=DATABASE.USERNAME,
                        new_value=value                        
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
