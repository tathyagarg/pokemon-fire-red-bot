import re
import discord
import database
import constants
from global_vars import *
from constants import BOT_DATA
from discord.ext import commands
from entities import pokemon as pokemon_events
from commons import (
    check_registered,
    check_registered_without_context
)

DATABASE: constants.Database = BOT_DATA.DATABASE

class Party(commands.Cog):
    def __init__(self, bot: BOT) -> None:
        self.bot: BOT = bot
    
    party: discord.commands.SlashCommandGroup = \
        discord.commands.SlashCommandGroup(name="party", description="Actions to navigate your party", guild_ids=BOT_DATA.GUILD_IDS)

    @party.command()
    @commands.check(check_registered)
    async def view(self, ctx: CTX, user: discord.User = None) -> None:
        if user:
            if not check_registered_without_context(user):
                await ctx.respond(f"The requested user has not registered!")
                return
            target: discord.User = user
        else:
            target: discord.User = ctx.author

        party: list[str] = database.request_field(uid=target.id, field=DATABASE.PARTY)
        
        embed: discord.Embed = discord.Embed(
            color=BOT_DATA.COLORS.COLOR_PRIMARY,
            title=f"{target.display_name}'s Party"
        )

        embed.set_thumbnail(url=target.avatar.url)

        for i, pokemon in enumerate(party, 1):
            pokemon: pokemon_events.PokemonInstance = pokemon_events.PokemonInstance.decode(encoded_string=pokemon)
            embed.add_field(name=f'Slot {i}', value=f"{pokemon.instance_of.discord_data.emoji} Level {pokemon.level} {pokemon.nick}", inline=True)

        await ctx.respond(embed=embed)

    @party.command()
    @commands.check(check_registered)
    async def info(self, ctx: CTX, slot: int, user: discord.User = None) -> None:
        if slot > 6 or slot < 1:
            await ctx.respond("Invalid slot number!")
            return

        if user:
            if not check_registered_without_context(user):
                await ctx.respond("The requested user has not registered!")
                return
            target: discord.User = user
        else:
            target: discord.User = ctx.author

        party: list[str] = database.request_field(uid=target.id, field=DATABASE.PARTY)

        if slot > len(party):
            await ctx.respond("The requested user does not have that many pokemon in their party!")
            return
        
        pokemon: pokemon_events.PokemonInstance = pokemon_events.PokemonInstance.decode(encoded_string=party[slot-1])

        embed: discord.Embed = discord.Embed(
            color=BOT_DATA.COLORS.COLOR_PRIMARY,
            title=f'{pokemon.instance_of.discord_data.emoji} {pokemon.nick}'
        )

        embed.add_field(name="Level", value=f'Lv. {pokemon.level}', inline=False)
        embed.add_field(name="Nature", value=f'{pokemon.nature}', inline=False)

        embed.add_field(name="IVs", value="\n".join(
            [f"**{k.replace('_', ' ').title() if k != 'hp' else 'HP'}**: {v}" for k, v in pokemon.ivs.__dict__.items()]
        ), inline=False)
        embed.add_field(name='Held Item', value=('None' if not pokemon.held_item else f'{pokemon.held_item.emoji} {pokemon.held_item}'), inline=False)
        embed.set_thumbnail(url=target.display_avatar.url)

        file = discord.File(fp=f'assets/info_sprites/{pokemon.instance_of.pokedex_number:0>3}_{pokemon.instance_of.name.lower().replace(" ", "_")}.png', filename='output.png')
        embed.set_image(url='attachment://output.png')

        await ctx.respond(embed=embed, file=file)

def setup(client: BOT) -> None:
    client.add_cog(cog=Party(bot=client))
