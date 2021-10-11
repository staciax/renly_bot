# Standard
import discord
from discord.ext import commands , tasks


class Help(commands.Cog, command_attrs = dict(slash_command=True)):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")

    @commands.command(slash_command=True , help="help commands")
    @commands.guild_only()
    async def help(self, ctx):
        embed = discord.Embed(description="help", color=0xffffff)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))