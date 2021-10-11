# Standard 
import discord
import os
from discord.ext import commands , tasks
from time import time
from datetime import datetime, timedelta, timezone
from typing import Literal

# Third party
# Local
from utils.emoji import emoji_converter
from utils.buttons import Confirm

class Owner(commands.Cog, command_attrs = dict(slash_command_guilds=[840379510704046151 , 893335017776894034 , 893335068863496192])):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")

    @commands.command(help="logout bot")
    @commands.is_owner()
    async def logout(self, ctx):
        embed = discord.Embed(color=0xffffff)
        embed.set_author(name=f"{self.bot.user.name} Logout",icon_url=self.bot.user.avatar.url)
        embed.description = f"are you sure?"

        view = Confirm()
        await ctx.send(embed=embed ,view=view)
        await view.wait()
        if view.value is None:
            return
        elif view.value:
            print('Shuting down...')
            await self.bot.logout()
        else:
            print('Cancelled...')


    @commands.command(name="bot_status",help="change bot status")
    @commands.is_owner()
    async def botstatus(
        self,
        ctx,
        type: Literal["playing", "streaming", "listening", "watching"] = commands.Option(description="status type"),
        status = commands.Option(description="Status text"),
        streaming_url = commands.Option(default=None, description="streaming status url"),
    ): 

        if type == "playing":  # Setting `Playing ` status
            await self.bot.change_presence(activity=discord.Game(name=status))
        elif type == "streaming": # Setting `Streaming ` status
            await self.bot.change_presence(activity=discord.Streaming(name=status, url=url))
        elif type == "listening": # Setting `Listening ` statu
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))
        elif type == "watching": # Setting `Watching ` status
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))
        
        embed = discord.Embed(title="Status Changed!",description=f"**type:** {type}\n**status:** `{status}`", color=self.bot.white_color)
        await ctx.send(embed=embed)
    
    @commands.command(help="enable command")
    @commands.is_owner()
    async def enable(self, ctx, command = commands.Option(description="command name")):
        command = self.bot.get_command(command)
        if command.enabled:
            return await ctx.send(f"`{command}` is already enabled.")
        command.enabled = True
        await ctx.send(f"Successfully enabled the `{command.name}` command.")
    
    @commands.command(help="disable command")
    @commands.is_owner()
    async def disable(self, ctx, command = commands.Option(description="command name")):
        command = self.bot.get_command(command)
        if not command.enabled:
            return await ctx.send(f"`{command}` is already disabled.")
        command.enabled = False
        await ctx.send(f"Successfully disabled the `{command.name}` command.")

    @commands.command(help="load cog")
    @commands.is_owner()
    async def load(self, ctx, extension = commands.Option(description="extension")):
        embed = discord.Embed()
        try:
            self.bot.load_extension(f'cogs.{extension}')
            embed.description = f"{emoji_converter('greentick')} Load : `{extension}`"
            embed.color = 0x8be28b
        except Exception as e:
            embed.description(f"Could not reload : `{extension}`")
            embed.color = 0xFF7878

        await ctx.send(embed=embed)
    
    @commands.command(help="unload cog")
    @commands.is_owner()
    async def unload(self, ctx, extension = commands.Option(description="extension")):
        embed = discord.Embed()
        try:
            self.bot.unload_extension(f'cogs.{extension}')
            embed.description = f"{emoji_converter('greentick')} Unload : `{extension}`"
            embed.color = 0x8be28b
        except Exception as e:
            embed.description(f"Could not reload : `{extension}`")
            embed.color = 0xFF7878

        await ctx.send(embed=embed)
    
    @commands.command(help="reload cog")
    @commands.is_owner()
    async def reload(self, ctx, extension= commands.Option(description="extension")):
        embed = discord.Embed()
        try:
            self.bot.unload_extension(f'cogs.{extension}')
            self.bot.load_extension(f'cogs.{extension}')
            embed.description = f"{emoji_converter('greentick')} Reload : `{extension}`"
            embed.color = 0x8be28b
        except Exception as e:
            embed.description(f"Could not reload : `{extension}`")
            embed.color = 0xFF7878

        await ctx.send(embed=embed)
    
    @commands.command(help="reload all cogs")
    @commands.is_owner()
    async def reloadall(self, ctx):
        embed = discord.Embed()
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and not filename.startswith("_"):
                if not filename == "owner.py":
                    try:
                        self.bot.reload_extension(f"cogs.{filename[:-3]}")
                        embed.description = f"{emoji_converter('greentick')} Reloaded all"
                        embed.color = 0x8be28b
                    except Exception as e:
                        self.bot.load_extension(f"cogs.{filename[:-3]}")
                        return await ctx.send(f"{e}")

        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Owner(bot))