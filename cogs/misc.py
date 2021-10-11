# Standard
import discord
import platform
from discord.ext import commands , tasks

from utils.emoji import emoji_converter
from utils.formats import format_dt , count_python


class Misc(commands.Cog, command_attrs = dict(slash_command=True)):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")

    @commands.command(help="Invite me")
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True , embed_links=True)
    async def invite(self, ctx):
        view = discord.ui.View()
        invite_button = discord.ui.Button(style=discord.ButtonStyle.gray, label="Invite me", url="") 
        view.add_item(item=invite_button)
        await ctx.send(view=view)
    
    @commands.command(help="Vote for me")
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True , embed_links=True)
    async def vote(self, ctx):
        view = discord.ui.View()
        vote_button = discord.ui.Button(style=discord.ButtonStyle.gray , label="Vote for me", url="") 
        view.add_item(item=vote_button)
        await ctx.send(view=view)
    
    @commands.command(help="Support server")
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True , embed_links=True)
    async def support(self, ctx):
        view = discord.ui.View()
        support_button = discord.ui.Button(style=discord.ButtonStyle.gray , label="Server support", url="") 
        view.add_item(item=support_button)
        await ctx.send(view=view)

    @commands.command(help="Bot prefix")
    @commands.guild_only()
    async def prefixes(self, ctx):
        await ctx.send(self.bot.defaul_prefix)
    
    @commands.command(aliases=["botinfo"])
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True , embed_links=True)
    async def about(self, ctx):
        owner_bot = self.bot.get_user(self.bot.owner_id) or (await self.bot.fetch_user(self.bot.owner_id))

        embed = discord.Embed(color=self.bot.white_color)
        embed.set_author(name=f"About Me",icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url=owner_bot.avatar.url)

        #stats
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))
        totalcogs = len(self.bot.cogs)
        totalcommands = len(self.bot.commands)

        #owner
        fields = [
            ("About Developer" , f"Owner:[{owner_bot}](https://discord.com/users/{owner_bot.id})" , False),
            ("Stats " , f"{self.bot.get_emoji(896576387002032159)} Line count : `{count_python('.'):,}`\n<:latteicon:870419352632045568> Servers : `{serverCount}`\n<:member:864219999954796615> Users : `{memberCount}`\n<:bot_commands:892297283532632116> Commands : `{totalcommands}`" , False), #{platform.system()}
            ("Bot Info" , "{emoji_converter('python')} Python : `{platform.python_version()}`\n{emoji_converter('dpy')} Discord.py : `{discord.__version__}`\n{emoji_converter('latteicon')} Latte : `{self.bot.bot_version}`\n{emoji_converter('mongodb')} Database : `PostgreSQL`" , False),
            ]
        for name , value , inline in fields:
            embed.add_field(name=name , value=value , inline=inline)

        embed.add_field(name="Bot created" , value=f"{format_dt(self.bot.user.created_at)}" , inline=inline)
                
        #start_view_button
        # view = discord.ui.View()
        # style = discord.ButtonStyle.gray
        #Source_code = discord.ui.Button(emoji=f"{utils.emoji_converter('github')}",style=style, label="Source code", url=self.bot.latte_source)
        #Vote.gg = discord.ui.Button(style=style, label="Source code", url=self.bot.latte_source)
        # view.add_item(item=Source_code)
    
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Misc(bot))