# Standard
import discord
import asyncio
import typing
from discord import Embed
from discord.ext import commands , tasks

# Third party
import requests
from PIL import Image , ImageColor
from io import BytesIO
from colorthief import ColorThief

# Local
from utils.paginator import SimplePages
from utils.custom_button import roleinfo_view , channel_info_view
from utils.emoji import profile_converter, emoji_converter , status_converter
from utils.converter import *
from utils.formats import format_dt

class Infomation(commands.Cog, command_attrs = dict(slash_command=True)):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")
    
    @commands.command(help="Show server infomation", aliases=["si", "serverinformation", "serverinformations" , "guildinfo" , "gi"], message_command=False)
    @commands.guild_only()
    async def server_info(self, ctx):

        #afk_channel_check and timeout
        afk_channels = afk_channel_check(ctx)      
        afk_timeouts = afk_channel_timeout(ctx)

        #member_status and emoji_member_status
        statuses = member_status(ctx)
        
        #emoji_count
        emoji_total = len(ctx.guild.emojis)
        emoji_regular = len([emoji for emoji in ctx.guild.emojis if not emoji.animated])
        emoji_animated = len([emoji for emoji in ctx.guild.emojis if emoji.animated])

        #boost_checker
        boost = check_boost(ctx)

        #dominant_colour_icon_guild
        try:
            url = ctx.guild.icon.replace(format='png')
            resp = requests.get(url)      
            out = BytesIO(resp.content)
            out.seek(0)
            icon_color = ColorThief(out).get_color(quality=1)
            icon_hex = '{:02x}{:02x}{:02x}'.format(*icon_color)
            dominant_color = int(icon_hex, 16)
        except:
            dominant_color = self.bot.white_color
           
        embed = discord.Embed(title=f"Server info - {ctx.guild.name}",color=dominant_color)
        fields = [("Server name",ctx.guild.name, True),
				("Server Owner",f"{ctx.guild.owner}", True),
                ("Server Region",str(ctx.guild.region).title(), True),
                ("Server Member",len([member for member in ctx.guild.members if not member.bot]), True),
                ("Server Bots",len([Member for Member in ctx.guild.members if Member.bot]), True),
                ("Server Roles",len(ctx.guild.roles), True),
                ("Text Channels",len(ctx.guild.text_channels), True),
                ("Voice Channels",len(ctx.guild.voice_channels), True),
                ("Stage Chennels",len(ctx.guild.stage_channels), True),
                ("Category size",len(ctx.guild.categories), True),
                ("AFK Chennels",afk_channels, True),
                ("AFK Timer",afk_timeouts,True),
                ("Rules Channel",rules_channel(ctx),True),
                ("System Channel",system_channel(ctx),True),
                ("Verification Level",guild_verification_level(ctx),True),
                ("Activity",f"{emoji_converter('member')} **Total:** {str(ctx.guild.member_count)}\n{status_converter('online')} **Online:** {statuses[0]} \n{status_converter('idle')} **Idle:** {statuses[1]} \n{status_converter('dnd')} **Dnd:** {statuses[2]} \n{status_converter('offline')} **Offline:** {statuses[3]}",True),
                ("Boosts",boost,True),
                ("Emoji",f"**Total:** {emoji_total}\n**Regular:** {emoji_regular}\n**Animated:** {emoji_animated}",True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_thumbnail(url=ctx.guild.icon.url)
    
        await ctx.send(embed=embed)
    
    @commands.command(name="user_info",help="Userinfomation", aliases=["userinfo","ui", "userinformation","memberinfo"])
    @commands.guild_only()
    async def user_info(self, ctx, member: discord.Member = commands.Option(description="Mention member")):
        member = member or ctx.author
        
        #member_status
        m_mobile = f"{status_converter(str(member.mobile_status))} Moblie"
        m_desktop = f"{status_converter(str(member.desktop_status))} Desktop"
        m_Web = f"{status_converter(str(member.web_status))} Web"
        
        #member_badge
        flags = member.public_flags.all()
        badges ="\u0020".join(profile_converter(f.name) for f in flags)
        if member.bot: badges = f"{badges} {profile_converter('bot')}"
        if member.premium_since: badges = f"{badges} {profile_converter('guildboost')}"

        #member_info
        member_joined = format_dt(member.joined_at, style='d')
        member_created = format_dt(member.created_at, style='d')
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        member_activity = f"{str(member.activity.type).title().split('.')[1]} {member.activity.name}" if member.activity is not None else "** **"
        roles = [role for role in member.roles]
        role_str = []
        if len(member.roles) > 1: role_string = ' '.join(reversed([r.mention for r in member.roles][1:]))
        else: role_string = "this user don't have a role"
        
        #fetch_banner
        fetch_member = await self.bot.fetch_user(member.id)
        #if fetchedMember.banner.is_animated() == True:

        #dominant_colour_user_info
        try:
            url = member.avatar.replace(format='png')
            resp = requests.get(url)      
            out = BytesIO(resp.content)
            out.seek(0)
            icon_color = ColorThief(out).get_color(quality=1)
            icon_hex = '{:02x}{:02x}{:02x}'.format(*icon_color)
            dominant_color = int(icon_hex, 16)
        except:
            if member.color == discord.Colour.default():
                dominant_color = member.colour

        #start_view
        view = discord.ui.View()
        style = discord.ButtonStyle.gray 

        embed = discord.Embed(title=f"{member}'s Infomation",colour=dominant_color)  #timestamp=ctx.message.created_at
        fields = [("Nickname",f"{member.display_name}", True),
                ("Is bot?","Yes" if member.bot else "No", True),
                ("Activity",member_activity, True),
                ("Join position",f"{str(members.index(member)+1)}/{ctx.guild.member_count}", True),
                ("Joined",f"{member_joined}", True),
                ("Registered",f"{member_created}", True),
                ("Status",f"{m_desktop}\n{m_mobile}\n{m_Web}", True),
                ("Badge",f"{badges}** **", True),
                ("Top Role",member.top_role.mention, False),
                ("Roles ({})\n".format(len(member.roles)-1), role_string , False)]

        for name , value , inline in fields:
            embed.add_field(name=name , value=value , inline=inline)

        if member.avatar.url is not None:
            embed.set_thumbnail(url=member.avatar.url)
            item = discord.ui.Button(style=style, label="Avatar URL", url=member.avatar.url)
            view.add_item(item=item)
        if fetch_member.banner:
            embed.set_image(url=fetch_member.banner.url)
            item2 = discord.ui.Button(style=style, label="Banner URL", url=fetch_member.banner.url) 
            view.add_item(item=item2)
        elif fetch_member.accent_color:
            embed.add_field(name=f"Banner color" , value=f"{fetch_member.accent_color} (HEX)", inline=False)
            embed.set_footer(text=f"ID: {member.id}")

        await ctx.send(embed=embed , view=view)
    
    @commands.command(help="Show server icon", aliases=["servericon","guildicon" ,"sic"], message_command=False)
    @commands.guild_only()
    async def server_icon(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title = f"{guild.name}'s Icon:")
        #start_view_button
        view = discord.ui.View()
        style = discord.ButtonStyle.gray
        try:
            #dominant_colour_icon_guild
            url = guild.icon.replace(format='png')
            resp = requests.get(url)      
            out = BytesIO(resp.content)
            out.seek(0)
            icon_color = ColorThief(out).get_color(quality=1)
            icon_hex = '{:02x}{:02x}{:02x}'.format(*icon_color)
            dominant_color = int(icon_hex, 16)
        except:
            dominant_color = self.bot.white_color
        try:
            embed.color = dominant_color
            embed.set_image(url = guild.icon.url)
            item = discord.ui.Button(style=style, label="Server icon URL", url=guild.icon.url)
        except:
            embed_fail = discord.Embed(description="Guild icon not found" , color=self.bot.white_color)
            return await ctx.send(embed=embed_fail)

        view.add_item(item=item)
        await ctx.send(embed = embed , view=view)

    
    @commands.command(help="Show server banner", aliases=["serverbanner","sb","guildbanner"], message_command=False)
    @commands.guild_only()
    async def server_banner(self, ctx):
        guild = ctx.guild
        try:
            embed = discord.Embed(title = f"{guild.name}'s Banner:", color=self.bot.white_color).set_image(url = guild.banner.url)
            #start_view_button
            view = discord.ui.View()
            style = discord.ButtonStyle.gray
            item = discord.ui.Button(style=style, label="Server banner URL", url=guild.banner.url)
            view.add_item(item=item)
            await ctx.send(embed = embed, view=view)
        except:
            embed = discord.Embed(description="Guild banner not found" , color=self.bot.white_color)
            await ctx.send(embed=embed)
    
    @commands.command(help="Show server splash", aliases=["splash","serversplash","ssp","invitebanner"], message_command=False)
    @commands.guild_only()
    async def server_splash(self, ctx):
        guild = ctx.guild
        try:
            embed = discord.Embed(title = f"{guild.name}'s Invite banner:", color=self.bot.white_color).set_image(url = guild.splash.url)
            #start_view_button
            view = discord.ui.View()
            style = discord.ButtonStyle.gray
            item = discord.ui.Button(style=style, label="Splash URL", url=guild.splash.url)
            view.add_item(item=item)
            await ctx.send(embed=embed , view=view)
        except:
            embed = discord.Embed(description="Guild splash not found" , color=self.bot.white_color)
            await ctx.send(embed=embed)

    @commands.command(help="Show avatar", aliases=["av"], message_command=False)
    @commands.guild_only()
    async def avatar(self, ctx, member: discord.Member = commands.Option(default=None, description="Mention member")):
        member = member or ctx.author

        #dominant_colour_avatar
        try:
            url = member.avatar.replace(format='png')
            resp = requests.get(url)      
            out = BytesIO(resp.content)
            out.seek(0)
            icon_color = ColorThief(out).get_color(quality=1)
            icon_hex = '{:02x}{:02x}{:02x}'.format(*icon_color)
            dominant_color = int(icon_hex, 16)
        except:
            dominant_color = self.bot.white_color

        embed = discord.Embed(title = f"{member.name}'s Avatar:", color=dominant_color)
        if member.avatar.url is not None:
            embed.set_image(url = member.avatar.url)
            #start_view_button
            view = discord.ui.View()
            style = discord.ButtonStyle.gray
            item = discord.ui.Button(style=style, label="Avatar URL", url=member.avatar.url)
            view.add_item(item=item)
            await ctx.send(embed = embed , view=view)
        else:
            embed.description = f"this user must have a avatar."
            await ctx.send(embed = embed)
    
    @commands.command(help="Show avatar", aliases=["sav"], message_command=False)
    @commands.guild_only()
    async def avatar_server(self, ctx, member: discord.Member = commands.Option(default=None, description="Mention member")):
        member = member or ctx.author

        embed = discord.Embed()
        if member.avatar != member.display_avatar:
            #dominant_colour_avatar_server
            try:
                url = member.display_avatar.replace(format='png')
                resp = requests.get(url)      
                out = BytesIO(resp.content)
                out.seek(0)
                icon_color = ColorThief(out).get_color(quality=1)
                icon_hex = '{:02x}{:02x}{:02x}'.format(*icon_color)
                dominant_color = int(icon_hex, 16)
            except:
                dominant_color = self.bot.white_color
            
            #display_avatar
            embed.title = f"{member.name}'s Server avatar:"
            embed.set_image(url = member.display_avatar.url)
            embed.color = dominant_color

            #start_view_button
            view = discord.ui.View()
            style = discord.ButtonStyle.gray
            item = discord.ui.Button(style=style, label="Server avatar URL", url=member.display_avatar.url)
            view.add_item(item=item)

            await ctx.send(embed = embed , view=view)
        else:
            embed.description = f"this user don't have a server avatar."
            embed.color = self.bot.white_color
            await ctx.send(embed = embed)

    @commands.command(help="Show banner", aliases=["bn"], message_command=False)
    @commands.guild_only()
    async def banner(self, ctx, member: discord.Member = commands.Option(default=None, description="Mention member")):
        member = member or ctx.author
        fetch_member = await self.bot.fetch_user(member.id)

        embed = discord.Embed(title=f"{member.name}'s Banner:")
        if fetch_member.banner:
            embed.set_image(url=fetch_member.banner.url)
            
            #dominant_colour_banner
            try:
                url = fetch_member.banner.replace(format='png')
                resp = requests.get(url)      
                out = BytesIO(resp.content)
                out.seek(0)
                icon_color = ColorThief(out).get_color(quality=1)
                icon_hex = '{:02x}{:02x}{:02x}'.format(*icon_color)
                dominant_color = int(icon_hex, 16)
            except:
                dominant_color = self.bot.white_color
            
            #dominant_color
            embed.color = dominant_color

            #start_view_button
            view = discord.ui.View()
            style = discord.ButtonStyle.gray
            item = discord.ui.Button(style=style, label="Banner URL", url=fetch_member.banner.url)
            view.add_item(item=item)
            await ctx.send(embed=embed , view=view)
        elif fetch_member.accent_color:
            img = Image.new("RGB", (256, 144), ImageColor.getrgb(f"{fetch_member.accent_color}"))
            buffer = BytesIO()
            img.save(buffer, 'png')
            buffer.seek(0)
            f = discord.File(buffer, filename='banner.png')

            embed.color = fetch_member.accent_color
            embed.set_image(url="attachment://banner.png")
            embed.add_field(name=f"this user don't have banner\n\nAccent color:" , value=f"{fetch_member.accent_color} (HEX)", inline=False)
            await ctx.send(file=f, embed=embed)
        else:
            embed.description = f"this user don't have a banner."
            await ctx.send(embed=embed, delete_after=10)
    
    @commands.command(aliases=["ri"],message_command=False)
    @commands.guild_only()
    async def role_info(self, ctx, role: discord.Role = commands.Option(description="Mention role")):
        embed_role = discord.Embed(color=role.color)
        role_perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in role.permissions if p[1]])
        info = f"""
        **Mention**: {role.mention}
        **ID**: {role.id}
        **Name**: {role.name}
        **Color**: {role.color}
        **Create**: {format_dt(role.created_at)}
        **Positon**: {role.position}
        **Members**: {len(role.members)}
        **Permission**: {role_perm_string}
        """
        embed_role.description = f"{info}"

        role_member_list = []

        for x in role.members:
            member_role = f"{x} | `{x.id}`"
            role_member_list.append(member_role)

        view = roleinfo_view(ctx=ctx, embed=embed_role, entries=role_member_list, role=role)
        await view.start()
    
    @commands.command(name="emoji_info" , aliases=["ei"], help="emoji infomation",message_command=False)
    @commands.guild_only()
    async def emoji_info(self, ctx, emoji: typing.Union[discord.Emoji, discord.PartialEmoji] = commands.Option(description="Emoji")):            
        try:
            emoji = await emoji.guild.fetch_emoji(emoji.id)
        except discord.NotFound:
            return await ctx.send("I could not find this emoji in the given guild.")

        is_managed = "Yes" if emoji.managed else "No"
        is_animated = "Yes" if emoji.animated else "No"
        requires_colons = "Yes" if emoji.require_colons else "No"
        creation_time = format_dt(emoji.created_at)
        can_use_emoji = (
            "Everyone"
            if not emoji.roles
            else " ".join(role.name for role in emoji.roles)
        )

        description = f"""
        **Name:** {emoji.name}
        **Id:** {emoji.id}
        **Author:** {emoji.user.mention}
        **Time Created:** {creation_time}
        **Guild Name:** {emoji.guild.name}
        **Guild Id:** {emoji.guild.id}
        """
        embed = discord.Embed(
            title=f"**Emoji Information for:** `{emoji.name}`",
            description=description,
            colour=self.bot.white_color,
        )
        embed.set_thumbnail(url=emoji.url)
        #start_view_button
        view = discord.ui.View()
        style = discord.ButtonStyle.gray
        item = discord.ui.Button(style=style, label="Emoji URL", url=emoji.url)
        view.add_item(item=item)
        await ctx.send(embed=embed , view=view)

    @commands.command(name="status", help="Status platform")
    @commands.guild_only()
    async def status_(self, ctx, member: discord.Member = commands.Option(description="Mention member")):

        m = status_converter(str(member.mobile_status))
        d = status_converter(str(member.desktop_status))
        w = status_converter(str(member.web_status))

        #embed
        embed = discord.Embed(color=member.colour)
        if member.display_avatar.url is not None:
            embed.set_author(name=member , icon_url=member.display_avatar.url)
        else:
            embed.set_author(name=member)
        embed.description = f"{d} Desktop\n{m} Mobile\n{w} Web"

        await ctx.send(embed=embed , ephemeral=True)
    
    @commands.command(help="channel infomation")
    @commands.guild_only()
    async def channel_info(self, ctx, channel: typing.Union[discord.TextChannel, discord.VoiceChannel] = commands.Option(default=None, description="Channel infomation")):
        embed = Embed(color=self.bot.white_color)
        embed.title = f"{channel.name}'s Info"
        if str(channel.type) == "voice": embed.add_field(
            name="infomation:",
            value=f"**Type:** voice channel\n**Birate:** {int(channel.bitrate / 1000)}kbps\n**Region:** {channel.rtc_region}\n**Connected:** {len(channel.members)} connected",
            inline=False
        )
        if str(channel.type) == "text": embed.add_field(
            name="infomation:", 
            value=f"**Type:** text channel\n**Topic** : {channel.topic}\n**NSFW** : {channel.nsfw}",
            inline=False
        )
        
        role_list = []
        member_list = []
        for role in channel.changed_roles:
            role_msg = f"{role.mention} | `{role.id}`"
            role_list.append(role_msg)
        for member in channel.members:
            member_msg = f"{member.name} | `{member.id}`"
            member_list.append(member_msg)
              
        embed.add_field(name="Category:" , value=f"{channel.category}" , inline=False)
        embed.add_field(name="Create date:" , value=f"{format_dt(channel.created_at)}" , inline=False)
        embed.set_thumbnail(url=channel.guild.icon.url)
        embed.set_footer(text=f"ID : {channel.id}")
        
        if str(channel.type) == 'text':
            view = channel_info_view(ctx=ctx, embed=embed, channel=channel, role_list=role_list, member_list=member_list)
            await view.start_text()
        if str(channel.type) == 'voice':
            view = channel_info_view(ctx=ctx, embed=embed, channel=channel, role_list=role_list, member_list=member_list)
            await view.start_voice()
    
def setup(bot):
    bot.add_cog(Infomation(bot))