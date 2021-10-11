# Standard 
import discord
from discord.ext import commands

# ----- BADGE CONVERTER ----- #

def profile_converter(name):
  names_to_emojis = {
    "staff" : "<:staff:893347826036265061>",
    "partner" : "<:partner:893346589521870888>",
    "hypesquad" : "<:hypesquad:893346589417042021>",
    "bug_hunter" : "<:bug_hunter:893346589861621830>",
    "hypesquad_bravery" : "<:bravery:893346589198929941>",
    "hypesquad_brilliance" : "<:brillance:893346589538652230>",
    "hypesquad_balance" : "<:balance:893346589345738763>", 
    "early_supporter" : "<:early_supporter:893346589769334844>",
    "system" : "<:system_badge:893351489366540318>",
    "bug_hunter_level_2" : "<:bug_hunter_level_2:893346589559636009>",
    "verified_bot" : "<:verified_bot1:893349183812165656><:verified_bot2:893349211293253662>",
    "verified_bot_developer" : "<:verified_bot_developer:893350052800651276>",
    "early_verified_bot_developer" : "<:early_verified_bot_developer:893350037847965756>",
    "discord_certified_moderator" : "<:certified_moderator:893350659410251817>",
    "bot" : "<:bot_1:893349778346348544><:bot_2:893349787175378944>",
    "guildboost" : "<:boost:893356419192082484><:nitro:893346589337329735>",
    "nitro" : "<:nitro:893346589337329735>",   
  }
  return names_to_emojis.get(name)


# ----- EMOJI CONVERTER ----- #

def emoji_converter(name):
  names_to_emojis = {
    "member" : "<:member:864219999954796615>",
  }
  return names_to_emojis.get(name)

# ----- STATUS INFO ----- #

def status_converter(name):
  names_to_status = {
    "online" : "<:online:896657842298310686>",
    "dnd" : "<:dnd:896657867246030888>",
    "idle" : "<:idle:896657886111989761>",
    "offline" : "<:offline:896657913291096074>",
  }
  return names_to_status.get(name)