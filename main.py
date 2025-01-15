import discord
from discord.ext import commands
from discord import app_commands
import requests
import random as rand

TOKEN = 'token'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready(): #同步指令到Discord
    print(f'已登錄為 {bot.user.name} ({bot.user.id})')
    await bot.tree.sync()

#-----------------------------------------------------------------------------------------------------------------------#

@bot.tree.command(name='readme', description='使用說明')
async def readme(interaction: discord.Interaction):
    await interaction.response.send_message('**二次元色龜專用\n未滿18歲禁止使用\nOnly For 18+ Adult**\n\n*Images Powered By Waifu.im\n\nMade By JRY*')

#-----------------------------------------------------------------------------------------------------------------------#

@bot.tree.command(name='iwantpic', description='取得圖片')
@app_commands.describe(tag='選擇類型')
@app_commands.choices(tag=[
    app_commands.Choice(name='Ass', value='ass'),
    app_commands.Choice(name='Hentai', value='hentai'),
    app_commands.Choice(name='Milf', value='milf'),
    app_commands.Choice(name='Oral', value='oral'),
    app_commands.Choice(name='Paizuri', value='paizuri'),
    app_commands.Choice(name='Ecchi', value='ecchi'),
    app_commands.Choice(name='Ero', value='ero')
])

async def iwantpic(interaction: discord.Interaction, tag: str):
    url = 'https://api.waifu.im/search'
    params = {
        'included_tags': [tag],
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        pic = data['images'][0].get('url', '未找到圖片')
        await interaction.response.send_message(pic)

    else:
        await interaction.response.send_message('圖片獲取失敗，請稍後再試。')

#-----------------------------------------------------------------------------------------------------------------------#

@bot.tree.command(name='random', description='隨機圖片')
async def random(interaction: discord.Interaction):
    url = 'https://api.waifu.im/search'
    tags = ['ass', 'hentai', 'milf', 'oral', 'paizuri', 'ecchi', 'ero']
    tag = rand.choice(tags)

    params = {
        'included_tags': [tag],
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        pic = data['images'][0].get('url', '未找到圖片')
        await interaction.response.send_message(pic)

    else:
        await interaction.response.send_message('圖片獲取失敗，請稍後再試。')
        
#-----------------------------------------------------------------------------------------------------------------------#

bot.run(TOKEN)
