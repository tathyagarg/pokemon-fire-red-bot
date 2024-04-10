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
        msg: INTERACTION = await ctx.respond(embed=commons.dialogue_default_embed)  # TODO: Add a default embed
        d: dialogue.Dialogue = dialogue.Dialogue(
            msg_id=msg.id,
            displays=[
                (data.PROFESSOR_OAK, 'Hello, there! Glad to meet you!', None),
                (data.PROFESSOR_OAK, 'Welcome to the world of Pokémon!', None),
                (data.PROFESSOR_OAK, 'My name is Oak.', None),
                (data.PROFESSOR_OAK, 'People affectionately refer to me as the Pokémon Professor.', None),
                (data.PROFESSOR_OAK, 'This world...', None),
                (data.NIDORAN, '...is inhabited far and wide by creatures called Pokémon.', None),
                (data.NIDORAN, 'For some people, Pokémon are pets. Others use them for battling.', None),
                (data.NIDORAN, 'As for myself...', None),
                (data.NIDORAN, 'I study Pokémon as a profession.', None),
                (data.PROFESSOR_OAK, 'But first, tell me a little about yourself.', None),
                (data.PROFESSOR_OAK, 'Now tell me.', commons.Input(
                        query='Are you a boy or a girl?',
                        action=lambda gender: database.update_field(
                            uid=ctx.author.id,
                            field=DATABASE.IS_MALE,
                            new_value=gender
                        ),
                        _filter=lambda value: (first in 'mb') if (first := value[0].lower()) in 'mfbg' else True,  # True signifies male (is_male)
                        placeholder='Enter only "male", "female", "boy", or "girl"'
                    )), (
                    lambda: database.fetch_player_intro_sprite(uid=ctx.author.id), 
                    'Let\'s begin with your name.',
                    commons.Input(
                        query='What is it?',
                        action=lambda name: database.update_field(
                            uid=ctx.author.id,
                            field=DATABASE.USERNAME,
                            new_value=name  
                        ),
                        _filter=str.title,
                        placeholder='Enter your name here.'
                    )
                ), (
                    lambda: database.fetch_player_intro_sprite(uid=ctx.author.id),
                    'Right... So your name is {}.',
                    None
                ), 
                (data.BLUE, 'This is my grandson.', None),
                (data.BLUE, 'He\'s been your rival since you both were babies.', commons.Input(
                    query='...Erm, what was his name now?',
                    action=lambda name: database.update_field(
                        uid=ctx.author.id,
                        field=DATABASE.OPPONENT,
                        new_value=name
                    ),
                    _filter=str.title
                )),
                (data.BLUE, 'That\'s right! I remember him now! His name is {}!', None),
                (lambda: database.fetch_player_intro_sprite(uid=ctx.author.id), lambda: f"{database.request_field(uid=ctx.author.id, field=DATABASE.USERNAME)}!", None),
                (lambda: database.fetch_player_intro_sprite(uid=ctx.author.id), 'Your very own Pokémon legend is about to unfold!', None),
                (lambda: database.fetch_player_intro_sprite(uid=ctx.author.id), 'A world of dreams and adventures with Pokémon awaits! Let\'s go!', None),
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
