# Standard 
import discord
from discord.ext import commands
from datetime import datetime, timedelta

# Local
from utils.formats import format_relative

def member_status(ctx):
    statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
				len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
				len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
				len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]    
    return statuses

def check_boost(ctx):
    format_relative = lambda dt: discord.utils.format_dt(dt, 'R')
    if ctx.guild.premium_tier != 0:
        boosts = f'**Level:** {ctx.guild.premium_tier}\n**Boosts:** {ctx.guild.premium_subscription_count}'
        last_boost = max(ctx.guild.members, key=lambda m: m.premium_since or ctx.guild.created_at)
        if last_boost.premium_since is not None:
            boosts = f'{boosts}\n**Last Boost:**\n{last_boost} ({format_relative(last_boost.premium_since)})'
    else:
        boosts_1 = f'**Level:** \n**Boosts:** '
        boosts = f'{boosts_1}\n**Last Boost:**\n'

    return boosts

def afk_channel_check(ctx):
    if ctx.guild.afk_channel: afk_channels = ctx.guild.afk_channel
    else: afk_channels = "⠀"
    return afk_channels

def afk_channel_timeout(ctx):
    if ctx.guild.afk_channel:
        if ctx.guild.afk_timeout: afk_time = f"{int(ctx.guild.afk_timeout / 60)} Minutes"
    else: afk_time = "⠀"
    return afk_time

def rules_channel(ctx):
    if ctx.guild.rules_channel is None: rs = "⠀"
    else: rs = ctx.guild.rules_channel.mention   
    return rs

def system_channel(ctx):
    if ctx.guild.system_channel is None: sy = "⠀"
    else: sy = ctx.guild.system_channel.mention
    return sy

def guild_verification_level(ctx):
    if str(ctx.guild.verification_level) == "none": gvl = "⠀"
    else: gvl = ctx.guild.verification_level
    return gvl