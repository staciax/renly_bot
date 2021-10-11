# Standard
import discord
from discord import Embed
from discord.ext import commands , tasks

# Third

# Local

class utility(commands.Cog, command_attrs = dict(slash_command=True)):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")

    @commands.command(help="Set your afk",slash_command=True)
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True , embed_links=True)
    async def afk(self, ctx,*, reason=None):
        embed = Embed(color=self.bot.white_color)
        if reason is None:
            reason = "personal problems"
        elif len(reason) > 100:
            embed.description = "**reason** is a maximum of 100 characters."
            return await ctx.reply(embed=embed, ephemeral=True)
        
        self.bot.afk_user[ctx.author.id] = reason
        embed.description = f"**{ctx.author}** I have set your afk: {reason}"

        await ctx.send(embed=embed)

    @commands.command(help="saybot", usage="<message>", slash_command_guilds=[840379510704046151])
    @commands.guild_only()
    async def saybot(
        self,
        ctx,
        message = commands.Option(description="message"),
        member: discord.Member = commands.Option(default=None, description="member")
    ):
        member = member or ctx.author

        webhook = await ctx.channel.create_webhook(name=member.display_name)
        await webhook.send(message, username=member.display_name, avatar_url=member.avatar.url)
        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
            await webhook.delete()
            await ctx.send("\u200b", ephemeral=True)

def setup(bot):
    bot.add_cog(utility(bot))