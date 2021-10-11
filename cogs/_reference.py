# Standard
import discord
from discord.ext import commands , tasks

# Third

# Local

class reference(commands.Cog, command_attrs = dict(slash_command=True)):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")

def setup(bot):
    bot.add_cog(reference(bot))