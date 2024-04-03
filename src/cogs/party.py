import discord
from discord.ext import commands
from constants import BOT_DATA
from commons import check_registered, check_registered_without_context
from database import run_sql
import re
from entities import pokemon as pokemon_events

DATABASE = BOT_DATA.DATABASE

def decode_party(party_encoded):
    return re.findall(r'(<[^<>]*[<]*[^<>]*[>]*[^<>]*>)', party_encoded)

class Party(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    party = discord.commands.SlashCommandGroup(name="party", description="Actions to navigate your party", guild_ids=BOT_DATA.GUILD_IDS)

    @party.command()
    @commands.check(check_registered)
    async def view(self, ctx, user: discord.User = None):
        if user:
            if not check_registered_without_context(user):
                await ctx.respond(f"The requested user has not registered!")
                return
            
            target = user
        else:
            target = ctx.author

        party_encoded = run_sql("SELECT {} FROM {} WHERE {}=?".format(DATABASE.PARTY, DATABASE.DB_NAME, DATABASE.USER_ID), (target.id,))[0][0]
        party = decode_party(party_encoded)
        
        embed = discord.Embed(
            color=BOT_DATA.COLORS.COLOR_PRIMARY,
            title=f"{target.display_name}'s Party"
        )

        for i, pokemon in enumerate(party, 1):
            pokemon = pokemon_events.PokemonInstance.decode(pokemon[1:-1])
            embed.add_field(name=f'Slot {i}', value=f"{pokemon.instance_of.discord_data.emoji} {pokemon.nick}", inline=True)

        await ctx.respond(embed=embed)

    @party.command()
    @commands.check(check_registered)
    async def info(self, ctx, slot: int, user: discord.User = None):
        if slot > 6 or slot < 1:
            await ctx.respond("Invalid slot number!")
            return

        if user:
            if not check_registered_without_context(user):
                await ctx.respond("The requested user has not registered!")
                return
            
            target = user
        else:
            target = ctx.author

        party_encoded = run_sql("SELECT {} FROM {} WHERE {}=?".format(DATABASE.PARTY, DATABASE.DB_NAME, DATABASE.USER_ID), (target.id,))[0][0]
        party = decode_party(party_encoded)

        if slot > len(party):
            await ctx.respond("The requested user does not have that many pokemon in their party!")
            return
        
        pokemon = pokemon_events.PokemonInstance.decode(party[slot-1][1:-1])

        embed = discord.Embed(
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

def setup(client):
    client.add_cog(Party(client))
