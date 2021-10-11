# Standard
import discord
import datetime
import asyncio
import time
import re
from discord.ext import commands , tasks
from datetime import datetime, timedelta, timezone

#check_message
async def do_removal(self, ctx, limit, predicate, *, before=None, after=None):
    if limit > 2000:
        return await ctx.send(f'Too many messages to search given ({limit}/2000)')

    if before is None:
        before = ctx.message
    else:
        before = discord.Object(id=before)

    if after is not None:
        after = discord.Object(id=after)

    try:
        deleted = await ctx.channel.purge(limit=limit, before=before, after=after, check=predicate)
    except discord.Forbidden as e:
        return await ctx.send('I do not have permissions to delete messages.')
    except discord.HTTPException as e:
        return await ctx.send(f'Error: {e} (try a smaller search?)')

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        time_regex = re.compile(r"(\d{1,5}(?:[.,]?\d{1,5})?)([smhd])")
        time_dict = {"h":3600, "s":1, "m":60, "d":86400}
        matches = time_regex.findall(argument.lower())
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k]*float(v)
            except KeyError:
                raise commands.BadArgument("{} is an invalid time-key! h/m/s/d are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time