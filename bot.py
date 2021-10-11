# Standard 
import discord
import json
import os
import datetime
import re
import asyncio
from discord.ext import commands , tasks
from os import environ
from os.path import join, dirname
from typing import Union, List, Optional

# Third party
import asyncpg
#import psycopg2
from dotenv import load_dotenv

# Local
from utils.json_loader import read_json , write_json

#json_loader
data = read_json('bot_var')

dotenv_path = join(dirname(__file__), 'settings.env')
load_dotenv(dotenv_path)
setting_env = os.getenv('SETTING', None)

# DEFAUL_PREFIX = "r"
# #get_prefix_server
# async def get_prefix(bot, message):
#     if not message.guild:
#         return commands.when_mentioned_or(DEFAUL_PREFIX)(bot,message)
         
#     prefix = await bot.db.fetch('SELECT prefix FROM guilds WHERE guild_id = $1', message.guild.id)
#     if len(prefix) == 0:
#         await bot.db.execute('INSERT INTO guilds(guild_id, prefix) VALUES ($1, $2)', message.guild.id, DEFAUL_PREFIX)
#         prefix = DEFAUL_PREFIX
#     else:
#         prefix = prefix[0].get("prefix")
#     return commands.when_mentioned_or(prefix)(bot,message)

class RenlyBot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        self.bot_version = "1.0.0"
        self.tester = ""
        self.github = ""
        self.defaul_prefix = '-'
        self.blacklisted_users = []
        self.afk_user = {}
        self.no_prefix = False
        self.latte_id = 887274968012955679
        self.bot_join = 893695417320087573
        self.bot_leave = 893695447309369345
        self.white_color = 0xffffff
        self.token = data["token"]
        self.owner_id = 240059262297047041
        super().__init__(command_prefix=commands.when_mentioned_or(self.defaul_prefix), *args, **kwargs)
    
    @property
    def renly(self) -> Optional[discord.User]:
        """Returns discord.User of the owner"""
        return self.get_user(self.owner_id)

    #thank_stella_bot
    def get_command_signature(self, ctx, command_name: Union[commands.Command, str]) -> str:
        if isinstance(command_name, str):
            if not (command := self.get_command(command_name)):
                raise Exception("Command does not exist for signature.")
        else:
            command = command_name
        return command #self.help_command.get_command_signature(command, ctx)
        
bot = RenlyBot(intents=discord.Intents(
    guild_reactions=True,  # reaction add/remove/clear
    guild_messages=True,  # message create/update/delete
    guilds=True,  # guild/channel join/remove/update
    integrations=True,  # integrations update
    voice_states=True,  # voice state update
    dm_reactions=True,  # reaction add/remove/clear
    guild_typing=True,  # on typing
    dm_messages=True,  # message create/update/delete
    presences=True,  # member/user update for games/activities
    dm_typing=True,  # on typing
    webhooks=True,  # webhook update
    members=True,  # member join/remove/update
    invites=True,  # invite create/delete
    emojis=True,  # emoji update
    bans=True  # member ban/unban
),help_command = None, case_insensitive = True , slash_commands= True, slash_command_guilds=[840379510704046151]) #, slash_command_guilds=[840379510704046151]
 
# botdata = {
#     "token": "this token",
#     "color": 0xffcccb,
#     "wtf": "testing",
# }
# a = testing(**botdata)

# @bot.command()
# async def set_prefix(ctx, new_prefix):
#     await bot.db.execute('UPDATE guilds SET prefix = $1 WHERE "guild_id" = $2', new_prefix, ctx.guild.id)
#     await ctx.send(f"set new prefix {new_prefix}")

@bot.event
async def on_ready():
    bot_avtivity = "Renly bot <3"
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name=bot_avtivity
    ))
    print(f"\nName : {bot.user}\nActivity : {bot_avtivity}\nServers : {len(bot.guilds)}\nUsers {len(set(bot.get_all_members()))}")
    print("\nCog loaded\n---------\n")

async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(host=data['dbhost'], user=data['dbuser'], password=data['dbpassword'], database=data['database'], min_size=1, max_size=5)
#    result = await bot.pg_con.fetch("SELECT * FROM public.guilds_prefix WHERE guild_id = $1;", guildid)
#    await bot.pg_con.execute("INSERT INTO public.guilds_prefix(guild_id, prefix)VALUES ($1, $2);", guild_id, new_prefix)
    print("connected to PostgreSQL")

#config_commands = message_command_only
#bot.load_extension('jishaku')

if __name__ == "__main__":
    for file in os.listdir("./cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f'cogs.{file[:-3]}')

bot.loop.run_until_complete(create_db_pool())
bot.run(bot.token , reconnect=True)