import discord
import database
from constants import BOT_DATA
from discord.ext import commands

class Basics(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.slash_command(
        guild_ids=BOT_DATA.GUILD_IDS
    )
    async def register(self, ctx):
        if database.check_user_exists(ctx.author.id):
            embed = discord.Embed(
                color=BOT_DATA.COLORS.COLOR_ERROR,
                title='User already registered',
                description='You are already registered!',
                thumbnail=ctx.author.avatar.url
            )

            embed.add_field(name='User', value=f'<@{ctx.author.id}>')

            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(
                color=BOT_DATA.COLORS.COLOR_SUCCESS,
                title='Successfully registered!',
                description='You have been successfully registered!',
                thumbnail=ctx.author.avatar.url
            )

            embed.add_field(name='User', value=f'<@{ctx.author.id}>')

            database.register_user(uid=ctx.author.id)
            await ctx.respond(embed=embed)

def setup(client):
    client.add_cog(Basics(client))
