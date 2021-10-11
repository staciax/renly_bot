# Standard
import discord
import typing
import random
from discord.ext import commands , tasks
from typing import Literal
# Third

# Local
from utils.api import base_waifu_im_api , base_waifu_pisc_api , base_waifu_pisc_api_nsfw , base_waifu_im_api_nsfw

class Api(commands.Cog, command_attrs = dict(slash_command=True)):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")
    
    @commands.command(help="Display waifu im.")
    @commands.guild_only()
    async def waifu_im(self, ctx, type: Literal["sfw", "nsfw"] = commands.Option(description="choose type")):
        if type == "sfw":
            waifu_url = "https://api.waifu.im/sfw/waifu/"
            view = base_waifu_im_api(ctx=ctx, url=waifu_url)
            return await view.api_start()
        elif type == "nsfw":
            if ctx.channel.is_nsfw():
                nsfw = ["ass","ecchi","ero","hentai","maid","milf","oppai","oral","paizuri","selfies","uniform"]
                random_nsfw = random.choice(nsfw)
                waifu_url = f"https://api.waifu.im/nsfw/{random_nsfw}/"
                view = base_waifu_im_api_nsfw(ctx=ctx, url=waifu_url)
                return await view.api_start()  
            raise commands.NSFWChannelRequired(ctx.channel)

    @commands.command(help="Display waifu pisc.")
    @commands.guild_only()
    async def waifu_pisc(self, ctx, type: Literal["sfw", "nsfw"] = commands.Option(description="choose type")):
        if type == "sfw":
            view = base_waifu_pisc_api(ctx=ctx)
            return await view.api_start()
        elif type == "nsfw":
            if ctx.channel.is_nsfw():
                view = base_waifu_pisc_api_nsfw(ctx=ctx)
                return await view.api_start()      
            raise commands.NSFWChannelRequired(ctx.channel)
            
def setup(bot):
    bot.add_cog(Api(bot))