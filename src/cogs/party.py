from discord.ext import commands

class Party(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    

def setup(client):
    client.add_cog(Party(client))
