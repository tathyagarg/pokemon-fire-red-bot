import re
import discord
import constants
from global_vars import *
from database import run_sql
from constants import BOT_DATA
from discord.ext import commands
from entities import pokemon as pokemon_events
from commons import (
    check_registered,
    check_registered_without_context
)

DATABASE: constants.Database = BOT_DATA.DATABASE

def decode_party(party_encoded: str) -> list[str]:
    return re.findall(r'(<[^<>]*[<]*[^<>]*[>]*[^<>]*>)', party_encoded)

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

        party_encoded: str = \
            run_sql(sql="SELECT {} FROM {} WHERE {}=?".format(DATABASE.PARTY, DATABASE.DB_NAME, DATABASE.USER_ID), values=(target.id,))[0][0]
        party: list[str] = decode_party(party_encoded=party_encoded)
        
        embed: discord.Embed = discord.Embed(
            color=BOT_DATA.COLORS.COLOR_PRIMARY,
            title=f"{target.display_name}'s Party"
        )

        embed.set_thumbnail(url=target.avatar.url)

        for i, pokemon in enumerate(party, 1):
            pokemon: pokemon_events.PokemonInstance = pokemon_events.PokemonInstance.decode(encoded_string=pokemon[1:-1])
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

        party_encoded: str = \
            run_sql(sql="SELECT {} FROM {} WHERE {}=?".format(DATABASE.PARTY, DATABASE.DB_NAME, DATABASE.USER_ID), values=(target.id,))[0][0]
        party: list[str] = decode_party(party_encoded=party_encoded)

        if slot > len(party):
            await ctx.respond("The requested user does not have that many pokemon in their party!")
            return
        
        pokemon: pokemon_events.PokemonInstance = pokemon_events.PokemonInstance.decode(encoded_string=party[slot-1][1:-1])

        embed: discord.Embed = discord.Embed(
            color=BOT_DATA.COLORS.COLOR_PRIMARY,
            title=f'{pokemon.instance_of.discord_data.emoji} {pokemon.nick}'
        )

        embed.add_field(name="Level", value=f'Lv. {pokemon.level}')
        embed.add_field(name="Nature", value=f'{pokemon.nature}')

        embed.add_field(name="IVs", value="\n".join(
            [f"**{k.replace('_', ' ').title()}**: {v}" for k, v in pokemon.ivs.__dict__.items()]
        ))
        embed.add_field(name='Held Item', value=('None' if not pokemon.held_item else f'{pokemon.held_item.emoji} {pokemon.held_item}'))
        embed.set_thumbnail(url=target.display_avatar.url)

        await ctx.respond(embed=embed)

def setup(client: BOT) -> None:
    client.add_cog(cog=Party(bot=client))
