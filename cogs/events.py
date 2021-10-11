# Standard
import discord
import random
import datetime
from discord import Embed
from discord.ext import commands , tasks
from datetime import datetime, timezone , timedelta
from typing import Literal

class Events(commands.Cog, command_attrs = dict(slash_command=True)):
    def __init__(self, bot):
        self.bot = bot
        if not hasattr(self.bot, 'commands_used'):
            self.bot.commands_used = 0
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")
        self.join_guild = self.bot.get_channel(self.bot.bot_join)
        self.leave_guild = self.bot.get_channel(self.bot.bot_leave)
        self.sniped = {}
        self.sniped_embed = {}
    
    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.bot.commands_used = self.bot.commands_used +1
        
        channel = self.bot.get_channel(844462710526836756)
        
        server = ctx.guild
        channel = ctx.channel
        owner = ctx.guild.owner
        author = ctx.author
        message = ctx.message
        
        colors = 0xffffff
        
        embed = discord.Embed(title=f"{ctx.command} has been used", color=self.bot.white_color, timestamp=discord.utils.utcnow())

        embed.description=f"""
        Server:
        Name: `{server}`
        ID: `{server.id}`
        Owner: `{owner}`

        User:
        Name: `{author}`
        hannel: `{channel}`
        URL: [Click here]({message.jump_url}/ 'Jump URL')
        Content:
        `{message.content}`
        """

        await channel.send(embed=embed)
                
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
                    
        for user_id in self.bot.afk_user.keys():
            if message.author.id == user_id:
                del self.bot.afk_user[user_id]
                return await message.channel.send(f"Welcome back {message.author.mention} , i've removed your **AFK** status." , delete_after=10)
            
            member = message.guild.get_member(user_id)
            if member.mentioned_in(message):
                embed = discord.Embed(description=f'**{member.display_name}** is afk for: {self.bot.afk_user[user_id]}' , color=self.bot.white_color)
                await message.channel.send(embed=embed , delete_after=15)

    @commands.Cog.listener()
    async def on_message_edit(self, before , after):       
        if before.content != after.content: 
            print(before.content , after.content)

    @commands.Cog.listener()
    async def on_message_delete(self, message):

        # if message.author.bot:
        #     return

        if message.content.startswith(f'{self.bot.defaul_prefix}snipe'):
            return

        self.sniped[message.guild.id] = message, message.content , message.author , message.channel , message.created_at 
    
        if message.embeds:
            self.sniped_embed[message.guild.id] = message.embeds[0]
      
    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def snipe(self, ctx , type: Literal["Message", "Embed"] = commands.Option(description="choose type")):

        embed = discord.Embed()
        embed.color = self.bot.white_color

        if type == 'Message':
            
            try:
                message , content, author, channel , time = self.sniped[ctx.guild.id]
            except:
                embed.description = "Couldn't find a message to snipe!"
                return await ctx.send(embed=embed, ephemeral=True)

            embed.timestamp = time
                            
            if content is not None or len(content) > 0:
                embed.description = content

            if author.avatar.url is not None:
                embed.set_author(name=f"{author} | {channel.name}", icon_url=author.avatar.url)
                
            elif author.avatar.url is None:
                embed.set_author(name=f"{author} | {channel.name}")
                
            if message.attachments:
                embed.set_image(url=message.attachments[0].url)

            await ctx.send(embed=embed, ephemeral=True)
        
        if type == 'Embed':
            try:
                embed_snipe = self.sniped_embed[ctx.guild.id]
            except:
                embed.description = "Couldn't find a embed to snipe!"
                return await ctx.send(embed=embed, ephemeral=True)

            await ctx.send(embed=embed_snipe , ephemeral=True)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        pass
    
    @commands.Cog.listener()
    async def on_invite_create(self, invite:discord.Invite):
        pass
    
    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        pass
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        pass
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        pass
        
    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        pass
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channels = [channel for channel in guild.channels]
        roles = roles= [role for role in guild.roles]
        embed = Embed(title="Bot just joined: "+str(guild.name), color=self.bot.white_color)
        embed.set_thumbnail(url = guild.icon.url)
        embed.add_field(name='Server Name:',value=f'{guild.name}')
        embed.add_field(name='Server ID:',value=f'{guild.id}')
        embed.add_field(name='Server region:',value=f'{guild.region}')
        embed.add_field(name='Server Creation Date:',value=f'{guild.created_at.strftime(r"%d/%m/%Y %H:%M")}')
        embed.add_field(name='Server Owner:',value=f'{guild.owner}')
        embed.add_field(name='Server Owner ID:',value=f'{guild.owner_id}')
        embed.add_field(name='Member Count:',value=f'{guild.member_count}')
        embed.add_field(name='Amount of Channels:',value=f"{len(channels)}")
        embed.add_field(name='Amount of Roles:',value=f"{len(roles)}")
        await self.join_guild.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channels = [channel for channel in guild.channels]
        roles = roles= [role for role in guild.roles]
        embed = Embed(title="Bot just left: "+str(guild.name), color=self.bot.white_color)
        embed.set_thumbnail(url = guild.icon.url)
        embed.add_field(name='Server Name:',value=f'{guild.name}')
        embed.add_field(name='Server ID:',value=f'{guild.id}')
        embed.add_field(name='Server region:',value=f'{guild.region}')
        embed.add_field(name='Server Creation Date:',value=f'{guild.created_at.strftime(r"%d/%m/%Y %H:%M")}')
        embed.add_field(name='Server Owner:',value=f'{guild.owner}')
        embed.add_field(name='Server Owner ID:',value=f'{guild.owner_id}')
        try:
            embed.add_field(name='Member Count:',value=f'{guild.member_count}')
        except:
            pass
        embed.add_field(name='Amount of Channels:',value=f"{len(channels)}")
        embed.add_field(name='Amount of Roles:',value=f"{len(roles)}")
        await self.leave_guild.send(embed=embed)

            
        


def setup(bot):
    bot.add_cog(Events(bot))