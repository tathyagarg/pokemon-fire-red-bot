import discord
from discord.ext import commands
from constants import BOT_DATA
from commons import check_registered
from database import run_sql
import re
from entities import pokemon as pokemon_events

DATABASE = BOT_DATA.DATABASE

class Party(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS)
    @commands.check(check_registered)
    async def party(self, ctx):
        party_encoded = run_sql("SELECT {} FROM {} WHERE {}=?".format(DATABASE.PARTY, DATABASE.DB_NAME, DATABASE.USER_ID), (ctx.author.id,))[0][0]
        party = re.findall(r'(<[^<>]*[<]*[^<>]*[>]*[^<>]*>)', party_encoded)
        
        embed = discord.Embed(
            color=BOT_DATA.COLORS.COLOR_PRIMARY,
            title=f"{ctx.author.display_name}'s Party"
        )

        for i, pokemon in enumerate(party, 1):
            pokemon = pokemon_events.PokemonInstance.decode(pokemon[1:-1])
            embed.add_field(name=f'Slot {i}', value=f"{pokemon.instance_of.discord_data.emoji} {pokemon.nick}", inline=True)

        await ctx.respond(embed=embed)

def setup(client):
    client.add_cog(Party(client))
