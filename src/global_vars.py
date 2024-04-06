import discord
import sqlite3
import discord.ext.commands

CTX = discord.commands.ApplicationContext
BOT = discord.ext.commands.bot.Bot
INTERACTION = discord.interactions.Interaction
CURSOR = sqlite3.Cursor