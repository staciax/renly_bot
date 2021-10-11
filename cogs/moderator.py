# Standard
import discord
import datetime
import asyncio
from discord.ext import commands , tasks
from datetime import datetime, timedelta, timezone

# Third
import requests

# Local
from utils.mod_converter import do_removal , TimeConverter
from utils.paginator import SimplePages

class Moderator(commands.Cog, command_attrs = dict(slash_command=True)):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")

    @commands.command(name="kick", help="kick member from your server", usage="<member> [reason]")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, ban_members=True)
    async def kick(self, ctx, member: discord.Member = commands.Option(description="Member"), reason= commands.Option(default=None, description="Reason")):
        if member == self.bot.user:
            return await ctx.send(embed=discord.Embed(description="you can't kick bot",color=self.bot.white_color))

        embed = discord.Embed(description=f'Member {member.mention} has been Kicked\nReason : {reason}', color=self.bot.white_color)

        await member.kick(reason=reason)
        await ctx.send(embed=embed)

    @commands.command(help="ban member from your server", usage="<member> [reason]")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, ban_members=True)
    async def ban(self, ctx, member: discord.Member = commands.Option(description="Member"), reason= commands.Option(default=None, description="Reason")):
        if member == self.bot.user:
            return await ctx.send(embed=discord.Embed(description="you can't kick bot",color=self.bot.white_color))
        
        embed = discord.Embed(description=f'{member} has been banned from server\nReason: {reason}', timestamp=datetime.now(timezone.utc),color=0xffffff)
        embed.set_footer(text=f"Banned by {ctx.author}" , icon_url = ctx.author.avatar.url)

        embedprm = discord.Embed(description="`Bot doesn't have enough permission to ban someone.`",color=self.bot.white_color)
       
        try:
            await member.ban(reason=reason)
            await ctx.send(embed=embed)
        except Exception:
            await ctx.send(embed=embedprm)
    
    @commands.command(help="Gets the current guild's list of bans")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, ban_members=True)
    async def bans(self, ctx) -> discord.Message:
        bans = await ctx.guild.bans()
        if not bans:
            return await ctx.send(embed=discord.Embed(description="There are no banned users in this server",color=self.bot.white_color))
        ban_list = []
        for ban_entry in bans:
            ban_list.append(f"{ban_entry.user}")
        p = SimplePages(entries=ban_list, per_page=10, ctx=ctx)
        p.embed.title = "Bans list"
        p.embed.color = self.bot.white_color
        await p.start()

    @commands.command(help="clear message")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True , send_messages=True, embed_links=True)
    async def clear(self, ctx, amount : int = commands.Option(description="Number to clear message")):
        embed = discord.Embed(
            description=f" `{ctx.channel.name}`: **{amount}** messages were cleared",
            color=self.bot.white_color
        )
        await ctx.channel.purge(limit=(int(amount) + 1))
        await ctx.reply(embed=embed, ephemeral=True)
    
    @commands.command(help="Cleanup the bot's messages")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True , send_messages=True, embed_links=True)
    async def cleanup(self, ctx , amount : int = commands.Option(description="Number to cleanup bot's message")):
        embed = discord.Embed(color=self.bot.white_color)
        try:
            await do_removal(self, ctx=ctx, limit=amount, predicate=lambda e: e.author == ctx.me)
            embed.description=f"`{ctx.channel.name}` : **{amount}** bot's messages were cleared"
        except:
            embed.description=f"i can't cleanup messages"
        await ctx.reply(embed=embed , ephemeral=True)

    # @commands.command(help="Mute member")
    # @commands.guild_only()
    # @commands.bot_has_permissions(manage_roles=True)
    # @commands.has_permissions(mute_members=True)
    # async def mute(
    #         self,
    #         ctx,
    #         member: discord.Member = commands.Option(description="Mention member"),
    #         time: TimeConverter = None,
    #         reason: str = commands.Option(default=None, description="reason")   
    #     ):

    #     if member == self.bot.user:
    #         return await ctx.send("can't mute bot")

    #     if time > 6000:
    #         return await ctx.send("i'm sorry it's in beta, you can't set the timer for more than 1 hour.")

    #     #mute_role
    #     role = discord.utils.get(ctx.guild.roles, name="Mute")#

    #     #embed
    #     embed = discord.Embed(color=self.bot.white_color)

    #     if not role:
    #         embed.description = "Your server don't have : **`Muted Role`**"
    #         return await ctx.send(embed=embed, ephemeral=True)

    #     if member == self.bot.user:
    #         embed.description = "You cannot mute the bot"
    #         return await ctx.send(embed=embed, ephemeral=True)
        
    #     if member == ctx.author:
    #         embed.description = "You cannot mute yourself."
    #         return await ctx.send(embed=embed, ephemeral=True)
                
    #     member_role = discord.utils.get(member.roles, name="Mute")
    #     if member_role:
    #         embed.description = "member's already have a mute role."
    #         return await ctx.send(embed=embed)

    #     try:
    #         await member.add_roles(role, reason=reason)
    #     except:
    #         embed.description = "i can't mute this member"
    #         return await ctx.send(embed=embed)
        
    #     if time:
    #         minutes, seconds = divmod(time, 60)
    #         hours, minutes = divmod(minutes, 60)
    #         msg_format = ""
    #         if hours: msg_format += f"{int(hours)} hours, "
    #         if minutes: msg_format += f"{int(minutes)} minutes, "
    #         if seconds : msg_format += f"{int(seconds)} seconds"
    #         embed.add_field(name="Time:", value=msg_format , inline=False)
        
    #     embed.description = f"mute member {member}"
    #     await ctx.send(embed=embed)

    #     if time and time < 6000:
    #         await asyncio.sleep(time)
    #         await member.remove_roles(role)

    # @commands.command(help="Unmute member")
    # @commands.guild_only()
    # @commands.bot_has_permissions(manage_roles=True)
    # @commands.has_permissions(mute_members=True)
    # async def unmute(
    #         self,
    #         ctx,
    #         member: discord.Member = commands.Option(description="Mention member")  
    #     ):
    #     role = discord.utils.get(ctx.guild.roles, name="Mute")

    #     embed = discord.Embed(description=f"You has been unmute : `{member}`",color=0xffffff)
    #     embed.set_footer(text=f"Unmuted by {ctx.author}", icon_url = ctx.author.avatar.url)

    #     await member.remove_roles(role)
    #     await ctx.send(embed=embed)
    
    # @commands.command(description="create mute role")
    # @commands.guild_only()
    # @commands.has_permissions(administrator = True)
    # async def muterole(self, ctx, role: discord.Role = commands.Option(description="Mention role")):
    #     await ctx.send(role)

    @commands.command(aliases=["nick"], help="change nickname", usage="<member> [new_name]")
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    async def change_nick(self, ctx , member: discord.Member = commands.Option(description="mention member"), nick:str = commands.Option(description="New nickname")):
        await member.edit(nick=nick)
        embed = discord.Embed(description=f"{member.mention} : Nickname was changed for `{member.display_name}`", color=self.bot.white_color)
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["slow"], help="set slowmode channel", usage="[seconds]")
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx , seconds: int = commands.Option(description="slowmode duration / seconds = 0 for disable")):
        embed = discord.Embed(color=self.bot.white_color)
        try:
            embed.description = f"Set the slowmode delay in this channel to {seconds} **seconds!**"
            await ctx.channel.edit(slowmode_delay=seconds)
        except:
            embed.description = f"i can't set the slowmode this channel"
            return await ctx.send(embed=embed)
        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Moderator(bot))