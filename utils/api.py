# Standard
import discord
from discord.ext import commands
from discord import Embed

# Third
import aiohttp

# Local

#-------------------- WAIFU IM --------------------#

    #----- base embed -----#

def Waifu_im_Embed(api_title, api_color, image_url):
    if api_title == "all": api_title = "random"
    embed = Embed(title=api_title, url=image_url, color=int(api_color)) #timestamp=discord.utils.utcnow(),
    embed.set_image(url=image_url)
    embed.set_footer(text="Powered by waifu.im")
    
    return embed

    #----- SFW -----#

class base_waifu_im_api(discord.ui.View):
    def __init__(self, ctx, url):
        super().__init__(timeout=600)
        self.ctx = ctx
        self.url = url
        self.image_url = ""
        self.message = ""

    def add_button(self):
        self.add_item(discord.ui.Button(label='Image URL', url=self.image_url))
    
    def api_site(self):
        self.add_item(discord.ui.Button(label='API site', url="https://waifu.im/"))

    async def on_timeout(self):
        self.clear_items()
        if self.message:
            await self.message.edit(view=self)
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user in (self.ctx.author, self.ctx.bot.renly):
            return True
        await interaction.response.send_message('This interaction cannot be controlled by you, sorry!', ephemeral=True)
        return False
    
    # @staticmethod
    # def Waifu_im_Embed(api_title, api_color, image_url):
    #     if api_title == "all": api_title = "random"
    #     embed = Embed(title=api_title, url=image_url, color=int(api_color)) #timestamp=discord.utils.utcnow(),
    #     embed.set_image(url=image_url)
    #     embed.set_footer(text="Powered by waifu.im")
        
    #     return embed
   
    @discord.ui.button(label='▶', style=discord.ButtonStyle.blurple, custom_id='b1')
    async def button_api(self, button: discord.ui.Button, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            request = await session.get(self.url)
            api = await request.json()
            if request.status == 200:
                api_title = api.get('tags')[0].get('name')
            
                #color_converter
                dominant_color1 = str(api.get('tags')[0].get('images')[0].get('dominant_color')).replace('#', '')
                dominant_color = int(dominant_color1, 16)

                api_color = dominant_color
                image_url = api.get('tags')[0].get('images')[0].get('url')
                self.image_url = image_url
 
            embed1 = Waifu_im_Embed(api_title, api_color, image_url)
            #embed1 = base_waifu_im_api.Waifu_im_Embed(api_title, api_color, image_url)
            for items in self.children:
                if isinstance(items, discord.ui.Button):
                    if items.label == "Image URL":
                        self.remove_item(item=items)
                        self.add_button()
                    
            await interaction.response.edit_message(embed=embed1, view=self)
    
    @discord.ui.button(emoji="❤️", style=discord.ButtonStyle.blurple, custom_id='b2')
    async def disable_all_button(self, button, interaction):
        self.clear_items()
        self.add_button()
        self.api_site()
        await interaction.response.edit_message(view=self)
        self.stop()

    @discord.ui.select(custom_id="Select_waifu_im", placeholder="Select category..", min_values=1, max_values=1, options=[
        discord.SelectOption(label='Waifu', value="waifu", description='Waifu'),
        discord.SelectOption(label='Maid', value="maid", description='Maid'),
        discord.SelectOption(label='Random', value="all", description='Random'),
    ])
    async def callback(self, select: discord.ui.select, interaction: discord.Interaction):
        if select.values[0]: self.url = f'https://api.waifu.im/sfw/{select.values[0]}'

    async def api_start(self):
        async with aiohttp.ClientSession() as session:
            request = await session.get(self.url)
            api = await request.json()
            if request.status == 200:
                api_title = api.get('tags')[0].get('name')
                
                #color_converter
                dominant_color1 = str(api.get('tags')[0].get('images')[0].get('dominant_color')).replace('#', '')
                dominant_color = int(dominant_color1, 16)

                api_color = dominant_color
                image_url = api.get('tags')[0].get('images')[0].get('url')
                
                self.image_url = image_url
                self.add_button()

        embed1 = Waifu_im_Embed(api_title, api_color, image_url)
        self.message = await self.ctx.reply(embed=embed1, view=self, mention_author=False)

    #----- NSFW -----#

class base_waifu_im_api_nsfw(discord.ui.View):
    def __init__(self, ctx, url):
        super().__init__(timeout=600)
        self.ctx = ctx
        self.url = url
        self.image_url = ""
        self.message = ""

    def add_button(self):
        self.add_item(discord.ui.Button(label='Image URL', url=self.image_url))
    
    def api_site(self):
        self.add_item(discord.ui.Button(label='API site', url="https://waifu.im/"))

    async def on_timeout(self):
        self.clear_items()
        if self.message:
            await self.message.edit(view=self)
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user in (self.ctx.author, self.ctx.bot.renly):
            return True
        await interaction.response.send_message('This interaction cannot be controlled by you, sorry!', ephemeral=True)
        return False
   
    @discord.ui.button(label='▶', style=discord.ButtonStyle.blurple, custom_id='b1')
    async def button_api(self, button: discord.ui.Button, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            request = await session.get(self.url)
            api = await request.json()
            if request.status == 200:
                api_title = api.get('tags')[0].get('name')
            
                #color_converter
                dominant_color1 = str(api.get('tags')[0].get('images')[0].get('dominant_color')).replace('#', '')
                dominant_color = int(dominant_color1, 16)

                api_color = dominant_color
                image_url = api.get('tags')[0].get('images')[0].get('url')
                self.image_url = image_url

        embed1 = Waifu_im_Embed(api_title, api_color, image_url)
        for items in self.children:
            if isinstance(items, discord.ui.Button):
                if items.label == "Image URL":
                    self.remove_item(item=items)
                    self.add_button()
                
        await interaction.response.edit_message(embed=embed1, view=self)
    
    @discord.ui.button(emoji="❤️", style=discord.ButtonStyle.blurple, custom_id='b2')
    async def disable_all_button(self, button, interaction):
        self.clear_items()
        self.add_button()
        self.api_site()
        await interaction.response.edit_message(view=self)
        self.stop()

    @discord.ui.select(custom_id="Select_waifu_im", placeholder="Select category..", min_values=1, max_values=1, options=[
        discord.SelectOption(label='Ass', value="ass", description='Waifu'),
        discord.SelectOption(label='Ecchi', value="ecchi", description='Maid'),
        discord.SelectOption(label='Ero', value="Ero", description='Random'),
        discord.SelectOption(label='Hentai', value="hentai", description='Random'),
        discord.SelectOption(label='Maid', value="maid", description='Random'),
        discord.SelectOption(label='Milf', value="milf", description='Random'),
        discord.SelectOption(label='Oppai', value="oppi", description='Random'),
        discord.SelectOption(label='Oral', value="oral", description='Random'),
        discord.SelectOption(label='Paizuri', value="paizuri", description='Random'),
        discord.SelectOption(label='Selfies', value="selfies", description='Random'),
        discord.SelectOption(label='Uniform', value="uniform", description='Random'),
    ])
    async def callback(self, select: discord.ui.select, interaction: discord.Interaction):
        if select.values[0]:
            self.url = f'https://api.waifu.im/nsfw/{select.values[0]}'
    
    async def api_start(self):
        async with aiohttp.ClientSession() as session:
            request = await session.get(self.url)
            api = await request.json()
            if request.status == 200:
                api_title = api.get('tags')[0].get('name')
                
                #color_converter
                dominant_color1 = str(api.get('tags')[0].get('images')[0].get('dominant_color')).replace('#', '')
                dominant_color = int(dominant_color1, 16)

                api_color = dominant_color
                image_url = api.get('tags')[0].get('images')[0].get('url')
                self.image_url = image_url
                self.add_button()

        embed1 = Waifu_im_Embed(api_title, api_color, image_url)
        self.message = await self.ctx.reply(embed=embed1, view=self, mention_author=False)

#-------------------- WAIFU PISC --------------------#

    #----- base embed -----#

def Waifu_pisc_Embed(self, json, title):
    embed = discord.Embed(title=title,url=json["url"], color=0xffffff)
    embed.set_image(url=json['url'])
    embed.set_footer(text="Powered by waifu.pisc")
 
    return embed

    #----- SFW -----#

class base_waifu_pisc_api(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=600)
        self.ctx = ctx
        self.url = "https://api.waifu.pics/sfw/waifu"
        self.json_url = ""
        self.title = "waifu"
        self.message = ""

    def add_button(self):
        self.add_item(discord.ui.Button(label='Image URL', url=self.json_url))

    def api_site(self):
        self.add_item(discord.ui.Button(label='API site', url="https://waifu.pics/"))

    async def on_timeout(self):
        self.clear_items()
        if self.message:
            await self.message.edit(view=self)
        
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user in (self.ctx.author, self.ctx.bot.renly):
            return True
        await interaction.response.send_message('This interaction cannot be controlled by you, sorry!', ephemeral=True)
        return False

    @discord.ui.button(label='▶', style=discord.ButtonStyle.blurple, custom_id='b1')
    async def button_api(self, button: discord.ui.Button, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            request = await session.get(self.url)
            api = await request.json()
            if request.status == 200:
                json = api
                self.json_url = json["url"]

        embed1 = Waifu_pisc_Embed(self, json, title=self.title)
        for items in self.children:
            if isinstance(items, discord.ui.Button):
                if items.label == "Image URL":
                    self.remove_item(item=items)
                    self.add_button()
                
        await interaction.response.edit_message(embed=embed1, view=self)

    @discord.ui.button(emoji="❤️", style=discord.ButtonStyle.blurple, custom_id='b2')
    async def disable_all_button(self, button, interaction):
        self.clear_items()
        self.add_button()
        self.api_site()
        await interaction.response.edit_message(view=self)
        self.stop()

    @discord.ui.select(custom_id="Select_waifu_pics_1", placeholder="Select category (A - K)", min_values=1, max_values=1, options=[        
        discord.SelectOption(label='Awoo', value="awoo", description='Waifu'),
        discord.SelectOption(label='Bite', value="bite", description='Waifu'),
        discord.SelectOption(label='Blush', value="blush", description='Waifu'),
        discord.SelectOption(label='Bonk', value="bonk", description='Waifu'),
        discord.SelectOption(label='bully', value="bully", description='Waifu'),
        discord.SelectOption(label='Cringe', value="cringe", description='Waifu'),
        discord.SelectOption(label='Cry', value="cry", description='Waifu'),
        discord.SelectOption(label='Cuddle', value="cuddle", description='Waifu'),
        discord.SelectOption(label='Dance', value="dance", description='Waifu'),
        discord.SelectOption(label='Glomp', value="glomp", description='Waifu'),
        discord.SelectOption(label='Handhold', value="handhold", description='Waifu'),
        discord.SelectOption(label='Happy', value="happy", description='Waifu'),
        discord.SelectOption(label='Highfive', value="highfive", description='Waifu'),
        discord.SelectOption(label='Hug', value="hug", description='Waifu'),
        discord.SelectOption(label='Kick', value="kick", description='Waifu'),
        discord.SelectOption(label='Kill', value="kill", description='Waifu'),
        discord.SelectOption(label='Kiss', value="kiss", description='Waifu'),
    ])
    async def callback_a_k(self, select: discord.ui.select, interaction: discord.Interaction):
        if select.values[0]:
            self.url = f'https://api.waifu.pics/sfw/{select.values[0]}'
            self.title = f'{str(select.values[0])}'
    
    @discord.ui.select(custom_id="Select_waifu_pics_2", placeholder="Select category (L - Z)", min_values=1, max_values=1, options=[
        discord.SelectOption(label='Lick', value="lick", description='Waifu'),
        discord.SelectOption(label='Megumin', value="megumin", description='Waifu'),
        discord.SelectOption(label='Neko', value="neko", description='Waifu'),
        discord.SelectOption(label='Nom', value="nom", description='Waifu'),
        discord.SelectOption(label='Pat', value="pat", description='Waifu'),
        discord.SelectOption(label='Poke', value="poke", description='Waifu'),
        discord.SelectOption(label='Shinobu', value="shinobu", description='Waifu'),
        discord.SelectOption(label='Slap', value="slap", description='Waifu'),
        discord.SelectOption(label='Smile', value="smile", description='Waifu'),
        discord.SelectOption(label='Smug', value="smug", description='Waifu'),
        discord.SelectOption(label='Waifu', value="waifu", description='Waifu'),
        discord.SelectOption(label='Wave', value="wave", description='Waifu'),
        discord.SelectOption(label='Wink', value="wink", description='Waifu'),
        discord.SelectOption(label='Yeet', value="yeet", description='Waifu'),
    ])
    async def callback_L_z(self, select: discord.ui.select, interaction: discord.Interaction):
        if select.values[0]:
            self.url = f'https://api.waifu.pics/sfw/{select.values[0]}'
            self.title = f'{str(select.values[0])}'
        
    async def api_start(self):
        async with aiohttp.ClientSession() as session:
            request = await session.get(self.url)
            api = await request.json()
            if request.status == 200:
                json = api
                self.json_url = json["url"]

        self.add_button()
        embed1 = Waifu_pisc_Embed(self, json, title=self.title)
        self.message = await self.ctx.reply(embed=embed1, view=self, mention_author=False)
    
    #----- NSFW -----#

class base_waifu_pisc_api_nsfw(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=600)
        self.ctx = ctx
        self.url = "https://api.waifu.pics/nsfw/waifu"
        self.json_url = ""
        self.title = "waifu"
        self.message = ""

    def add_button(self):
        self.add_item(discord.ui.Button(label='Image URL', url=self.json_url))

    def api_site(self):
        self.add_item(discord.ui.Button(label='API site', url="https://waifu.pics/"))

    async def on_timeout(self):
        self.clear_items()
        if self.message:
            await self.message.edit(view=self)
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user in (self.ctx.author, self.ctx.bot.renly):
            return True
        await interaction.response.send_message('This interaction cannot be controlled by you, sorry!', ephemeral=True)
        return False

    @discord.ui.button(label='▶', style=discord.ButtonStyle.blurple, custom_id='b1')
    async def button_api(self, button: discord.ui.Button, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            request = await session.get(self.url)
            api = await request.json()
            if request.status == 200:
                json = api
                self.json_url = json["url"]

        embed1 = Waifu_pisc_Embed(self, json, title=self.title)
        for items in self.children:
            if isinstance(items, discord.ui.Button):
                if items.label == "Image URL":
                    self.remove_item(item=items)
                    self.add_button()
                    
        await interaction.response.edit_message(embed=embed1, view=self)

    @discord.ui.button(emoji="❤️", style=discord.ButtonStyle.blurple, custom_id='b2')
    async def disable_all_button(self, button, interaction):
        self.clear_items()
        self.add_button()
        self.api_site()
        await interaction.response.edit_message(view=self)
        self.stop()

    @discord.ui.select(custom_id="Select_waifu_pics_1", placeholder="Select category (A - K)", min_values=1, max_values=1, options=[        
        discord.SelectOption(label='Waifu', value="waifu", description='Waifu'),
        discord.SelectOption(label='Neko', value="neko", description='Waifu'),
        discord.SelectOption(label='Trap', value="trap", description='Waifu'),
        discord.SelectOption(label='Blowjob', value="blowjob", description='Waifu')
    ])
    async def callback_a_k(self, select: discord.ui.select, interaction: discord.Interaction):
        if select.values[0]:
            self.url = f'https://api.waifu.pics/nsfw/{select.values[0]}'
            self.title = f'{str(select.values[0])}'
    
    async def api_start(self):
        async with aiohttp.ClientSession() as session:
            request = await session.get(self.url)
            api = await request.json()
            if request.status == 200:
                json = api
                self.json_url = json["url"]

        self.add_button()
        embed1 = Waifu_pisc_Embed(self, json, title=self.title)
        self.message = await self.ctx.reply(embed=embed1, view=self, mention_author=False)