import discord
import database
from global_vars import *
from constants import BOT_DATA
from discord.ext import commands

class Basics(commands.Cog):
    def __init__(self, bot: BOT) -> None:
        self.bot: BOT = bot

    @commands.slash_command()
    async def ping(self, ctx: CTX) -> None:
        await ctx.respond(f"Pong! The bot\'s latency sits as {self.bot.latency}")

    @commands.slash_command(guild_ids=BOT_DATA.GUILD_IDS)
    async def register(self, ctx: CTX) -> None:
        if database.check_user_exists(ctx.author.id):
            embed: discord.Embed = discord.Embed(
                color=BOT_DATA.COLORS.COLOR_ERROR,
                title='User already registered',
                description='You are already registered!',
                thumbnail=ctx.author.avatar.url
            )

            embed.add_field(name='User', value=f'<@{ctx.author.id}>')

            await ctx.respond(embed=embed)
        else:
            embed: discord.Embed = discord.Embed(
                color=BOT_DATA.COLORS.COLOR_SUCCESS,
                title='Successfully registered!',
                description='You have been successfully registered!',
                thumbnail=ctx.author.avatar.url
            )

            embed.add_field(name='User', value=f'<@{ctx.author.id}>')

            database.register_user(uid=ctx.author.id)
            await ctx.respond(embed=embed)

def setup(client: BOT) -> None:
    client.add_cog(cog=Basics(bot=client))
