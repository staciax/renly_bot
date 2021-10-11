# Standard
import discord
import traceback
import asyncio
import typing
import datetime
from typing import Literal
from discord.ext import commands , tasks, menus

# Third

# Local

from utils.paginator import SimplePages

class TagPageEntry:
    __slots__ = ('tag_id', 'name')
    def __init__(self, entry):
        self.tag_id = entry['tag_id']
        self.name = entry['name']

    def __str__(self):
        return f'{self.name} (ID: {self.tag_id})'

class TagPages(SimplePages):
    def __init__(self, entries, *, ctx: commands.Context, per_page: int = 12):
        converted = [TagPageEntry(entry) for entry in entries]
        super().__init__(converted, per_page=per_page, ctx=ctx)

class TagName(commands.clean_content):
    def __init__(self, *, lower=False):
        self.lower = lower
        super().__init__()

    async def convert(self, ctx, argument):
        converted = await super().convert(ctx, argument)
        lower = converted.lower().strip()

        if not lower:
            raise commands.BadArgument('Missing tag name.')

        if len(lower) > 100:
            raise commands.BadArgument('Tag name is a maximum of 100 characters.')

        return converted if not self.lower else lower

class Tags(commands.Cog, command_attrs = dict(slash_command=True)):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__}")

    async def get_tag(self, guild_id, name, *, connection=None):
        def get_match(rows , tag_name):
            if rows is None or len(rows) == 0:
                raise RuntimeError('Tag not found.')

            names = '\n'.join(r['name'] for r in rows)
            raise RuntimeError(f'Tag not found. Did you mean...\n`{names}`')

        con = connection or self.bot.pg_con

        query = "SELECT * FROM public.tags WHERE (name , guild_id) = ($1,$2);"
        row = await con.fetchrow(query, name, guild_id)
        if row is None:
            query = "SELECT * FROM public.tags WHERE guild_id = $1 AND name % $2 ORDER BY similarity(name, $2) LIMIT 3;"
            return get_match(await con.fetch(query, guild_id , name), tag_name=name)
        else:
            return row

    async def create_tag(self, ctx, name, content, owner, guild, connection=None):
        
        con = connection or self.bot.pg_con

        #check_tag
        query = "SELECT * FROM public.tags WHERE (name , guild_id) = ($1,$2);"
        row = await con.fetchrow(query, name, guild)
        if row:
            if row['name'] == str(name):
                return await ctx.send('This tag already exists.')

        #create_tag
        try:
            date_create = datetime.datetime.now()
            dt = date_create.replace(tzinfo=None)
            query = "INSERT INTO public.tags(name, content, owner_id, guild_id, use, created_at) VALUES ($1,$2,$3,$4,$5,$6);"
            await con.execute(query, name,content,owner, guild, 0 , dt)
            await ctx.send(f'Tag {name} successfully created.')
        except:
            return await ctx.send('Could not create tag.')
    
    @commands.command(help="tag command")
    @commands.guild_only()
    async def tag(self, ctx, name = commands.Option(description="Input name")):
        try:
            tag = await self.get_tag(guild_id=ctx.guild.id, name=name , connection=self.bot.pg_con)
        except RuntimeError as e:
            return await ctx.send(e)
        await ctx.send(tag['content'])

        if tag['content']==str(name):
            await self.bot.pg_con.execute("UPDATE public.tags SET use = $1 WHERE guild_id = $2 and name = $3;", tag['use']+1, ctx.guild.id, name)
            print("use +1")
    
    @commands.group(invoke_without_command=True , name="tags")
    @commands.guild_only()
    async def tags(self, ctx):
        pass

    @tags.command(name="create", help="Creates a new tag owned by you.")
    @commands.guild_only()
    async def tag_create(self, ctx, name: TagName(lower=True) = commands.Option(description="name of tag") , content: commands.clean_content = commands.Option(description="Content")):       
        if len(content) > 2000:
            return await ctx.send('Tag content is a maximum of 2000 characters.')

        guild_check = await self.bot.pg_con.fetch("SELECT * FROM public.tags WHERE guild_id = $1", ctx.guild.id)
        if len(guild_check)>=50:
            return await ctx.send("This server more than 50 tags at the moment. Please delete your old ones that are unused")
        
        await self.create_tag(ctx=ctx, name=name, content=content, owner=ctx.author.id, guild=ctx.guild.id , connection=self.bot.pg_con)
    
    @tags.command(name="remove", help="Remove tag")
    @commands.guild_only()
    async def tag_remove(self, ctx, name: TagName(lower=True) = commands.Option(description="name of tag")):
        owner = ctx.author.id
        guild = ctx.guild.id
        query = "SELECT * FROM public.tags WHERE (name , guild_id) = ($1,$2);"
        row = await self.bot.pg_con.fetchrow(query, name, guild)
        if row != None:
            if row['owner_id'] == owner:
                try:
                    query = "DELETE FROM public.tags WHERE (name , guild_id, owner_id) = ($1,$2,$3);"
                    await self.bot.pg_con.execute(query, name, guild , owner)
                    await ctx.send("You have successfully deleted your tag.")
                except:
                    await ctx.send('Could not delete tag. Please try again!')

            elif ctx.author.guild_permissions.administrator:
                try:
                    query = "DELETE FROM public.tags WHERE (name , guild_id) = ($1,$2);"
                    await self.bot.pg_con.execute(query, name, guild)
                    await ctx.send("You have successfully deleted this tag.")
                except:
                    await ctx.send('Could not delete tag. Please try again!')
            else:
                await ctx.send('You are not owner this tag!')
        else:
            await ctx.send(f'Tag not found!')
    
    @tags.command(name="edit", help="edit tag")
    @commands.guild_only()
    async def tag_edit(self, ctx, name: TagName(lower=True) = commands.Option(description="name of tag"), content: commands.clean_content = commands.Option(description="content")):
        query = "SELECT * FROM public.tags WHERE (name , guild_id , owner_id) = ($1,$2,$3);"
        row = await self.bot.pg_con.fetchrow(query, name, ctx.guidl.id , ctx.author.id)
        if row['name'] == name:
            await self.bot.pg_con.execute("UPDATE public.tags SET content = $1 WHERE guild_id = $2 and owner_id = $3 and name = $4", content, ctx.guild.id, ctx.author.id, name)
            return await ctx.send("You have successfully edited your tag.")
        await ctx.send("Could not find a tag with that name in your tags.")

    @tags.command(name="rename", help="rename tag")
    @commands.guild_only()
    async def tag_rename(self, ctx, old_name: TagName(lower=True) = commands.Option(description="tag old name"), new_name: TagName = commands.Option(description="tag new name")):
        query = "SELECT * FROM public.tags WHERE (name , guild_id , owner_id) = ($1,$2,$3);"
        row = await self.bot.pg_con.fetchrow(query, old_name, ctx.guidl.id , ctx.author.id)
        if row['name'] == old_name:
            await self.bot.pg_con.execute("UPDATE public.tags SET name = $1 WHERE guild_id = $2 and owner_id = $3 and name = $4", new_name, ctx.guild.id, ctx.author.id, old_name)
            return await ctx.send("You have successfully edited your tag.")
        await ctx.send("Could not find a tag with that name in your tags.")
    
    @tags.command(name="list", help="Show tag list from member")
    @commands.guild_only()
    async def tag_list(self, ctx, member: discord.Member = commands.Option(default=None, description="mention member")):
        member = member or ctx.author

        query = "SELECT name, tag_id FROM public.tags WHERE guild_id = $1 AND owner_id = $2 ORDER BY name"

        rows = await self.bot.pg_con.fetch(query, ctx.guild.id, member.id)

        if rows:
            p = TagPages(entries=rows, ctx=ctx , per_page=10)
            p.embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
            p.embed.color = self.bot.white_color
            await p.start()
        else:
            await ctx.send(f'{member} has no tags.')
    
    @tags.command(name="all", help="Show all tag from server")
    @commands.guild_only()
    async def tag_all(self, ctx):
        query = "SELECT name, tag_id FROM public.tags WHERE guild_id = $1 ORDER BY name"
        rows = await self.bot.pg_con.fetch(query, ctx.guild.id)

        if rows:
            p = TagPages(entries=rows, ctx=ctx , per_page=10)
            p.embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)
            p.embed.color = self.bot.white_color
            await p.start()
        else:
            await ctx.send(f"This server doesn't have any tags.")
    
    @tags.command(name="search",help="Search tag")
    @commands.guild_only()
    async def tag_search(self, ctx, tag: TagName(lower=True) = commands.Option(description="name of tag")):
        query = "SELECT * FROM public.tags WHERE guild_id = $1 AND name % $2 ORDER BY similarity(name, $2) LIMIT 20;"
        results = await self.bot.pg_con.fetch(query, ctx.guild.id , tag)
        
        if results:
            p = TagPages(entries=results, per_page=10, ctx=ctx)
            p.embed.color = self.bot.white_color
            await p.start()
        else:
            await ctx.send("This server doesn't have any tags.")

    @tags.command(name="info",help="Search tag")
    @commands.guild_only()
    async def tag_info(self, ctx, tag: TagName(lower=True) = commands.Option(description="name of tag")):
        query = "SELECT * FROM public.tags WHERE (name , guild_id) = ($1,$2);"
        record = await self.bot.pg_con.fetchrow(query, tag , ctx.guild.id)

        if record is None:
            return await ctx.send('Tag not found.')

        owner_id = record['owner_id']

        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.title = record['name']
        embed.timestamp = record['created_at'].replace(tzinfo=None)
        embed.set_footer(text='Tag created at')

        user = self.bot.get_user(owner_id) or (await self.bot.fetch_user(owner_id))
        embed.set_author(name=str(user), icon_url=user.display_avatar.url)

        embed.add_field(name='Owner', value=f'<@{owner_id}>')
        embed.add_field(name='Uses', value=record['use'])
        
        await ctx.send(embed=embed)

    @tags.command(name="remove_id")
    @commands.guild_only()
    async def tag_remove_by_id(self, ctx , id:int = commands.Option(description="Tag id")):
        owner = ctx.author.id
        query = "SELECT * FROM public.tags WHERE (tag_id , guild_id) = ($1,$2);"
        row = await self.bot.pg_con.fetchrow(query, id, ctx.guild.id)

        if row != None:
            if row['owner_id'] == owner or ctx.author.guild_permissions.administrator:
                try:
                    query = "DELETE FROM public.tags WHERE (tag_id , guild_id) = ($1,$2);"
                    await self.bot.pg_con.execute(query, id, ctx.guild.id)
                    return await ctx.send("You have successfully deleted tag.")
                except:
                    return await ctx.send('Could not delete tag. Please try again!')

            await ctx.send('You are not owner this tag!')
        else:
            await ctx.send(f'Tag not found!')


    "add cooldown all command"


def setup(bot):
    bot.add_cog(Tags(bot))