# Standard
import discord
from discord.ext import commands , tasks

import typing
from typing import Literal
# Third
import aiohttp

# Local
from utils.paginator import RoboPages
from utils.buttons import *

class Tesing(commands.Cog, command_attrs = dict(slash_command=True)):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")

    # @commands.command()
    # async def permtest(self, ctx):
    #     if ctx.author.guild_permissions.administrator:
    #         await ctx.send("admin")
    #     else:
    #         await ctx.send("member")

    # @commands.command()
    # async def api_test(self, ctx):
    #     async with aiohttp.ClientSession() as cs:
    #         async with cs.get("https://api.waifu.im/sfw/waifu/") as rep:
    #             api = await rep.json()
    #             print(api)

    # @commands.command(slash_command=True, help="Calculate a math expression", aliases=["calc"])
    # async def calculate(
    #     self,
    #     ctx,
    #     no_commas: typing.Optional[typing.Literal["true"]]=commands.Option(default=None, description="Whether to disable commas in the result or not"),
    #     debug: typing.Optional[typing.Literal["true"]]=commands.Option(default=None, description="Whether to show debug info or not"),
    #     *,
    #     args=commands.Option(default=None, description="Input an arguments")):
    #     if no_commas:
    #         await ctx.send("no_commas")
    #     elif debug:
    #         await ctx.send("debug")
    #     elif args:
    #         await ctx.send("args")

    # @commands.command()
    # async def ping2(self, ctx, type: Literal["db", "m", "t", "e"] = commands.Option(default=None, description="Type to ping. Options: typing, edit, message, database.")):
    #     if name:
    #         await ctx.send(name)

    #     if type == "m":
    #         await ctx.send("m")
    #     else:
    #         await ctx.send(type)

    # @commands.group()
    # async def tag(self, ctx, name):
    #     await ctx.send("test")
    
    # #add   
    # @tag.command(name="add")
    # async def tag_add(self ,ctx): 
    #     await ctx.send("add")

    # @tag.command(name="remove")
    # async def tag_remove(self, ctx): 
    #     await ctx.send("remove")

    # #edit   
    # @tag.group(invoke_without_command=True)
    # async def edit(self): 
    #     pass
    
    # @edit.command(name="content")
    # async def tag_edit_content(self ,ctx , name):
    #     await ctx.send(name)
    
    # @edit.command(name="alias")
    # async def tag_edit_alias(self ,ctx , name):
    #     await ctx.send(name)

    # @bot.command()
# async def ping(
#     ctx: commands.Context, emoji: bool = commands.Option(description="whether to use an emoji when responding")
# ):
#     if emoji:
#         await ctx.send("\U0001f3d3")
#     else:
#         await ctx.send("Pong!")

# @bot.command(message_command=False)
# async def only_slash(ctx: commands.Context):
#     await ctx.send("Hello from slash commands!")

# @bot.command(slash_command=False)
# async def only_message(ctx: commands.Context):
#     await ctx.send("Hello from message commands!")

def setup(bot):
    bot.add_cog(Tesing(bot))