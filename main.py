import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import random as rand
import logging

# 設定日誌記錄
logging.basicConfig(level=logging.INFO)

TOKEN = 'TOKEN'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

async def fetch_waifu_image(tag: str = None):
    url = 'https://api.waifu.im/search'
    params = {'included_tags': [tag]} if tag else {}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    return None, f"API 錯誤 (狀態碼: {response.status})"
                
                data = await response.json()
                if not data.get('images') or len(data['images']) == 0:
                    return None, "未找到符合條件的圖片"
                return data['images'][0].get('url'), None
                
    except (aiohttp.ClientError, ValueError) as e:
        logging.error(f"請求失敗: {str(e)}")
        return None, "圖片獲取失敗，請稍後再試。"

#-----------------------------------------------------------------------------------------------------------------------#

@bot.event
async def on_ready():
    print(f'已登錄為 {bot.user.name} ({bot.user.id})')
    try:
        await bot.tree.sync()
    except Exception as e:
        logging.error(f"指令同步失敗: {str(e)}")

#-----------------------------------------------------------------------------------------------------------------------#

@bot.tree.command(name='readme', description='使用說明')
async def readme(interaction: discord.Interaction):
    await interaction.response.send_message(
        '**二次元色龜專用\n未滿18歲禁止使用\nOnly For 18+ Adult**\n\n*Images Powered By Waifu.im\n\nMade By JRY*'
    )

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
    image_url, error = await fetch_waifu_image(tag)
    if error:
        await interaction.response.send_message(error)
    else:
        await interaction.response.send_message(image_url)

#-----------------------------------------------------------------------------------------------------------------------#

@bot.tree.command(name='random', description='隨機圖片')
async def random(interaction: discord.Interaction):
    tags = ['ass', 'hentai', 'milf', 'oral', 'paizuri', 'ecchi', 'ero']
    image_url, error = await fetch_waifu_image(rand.choice(tags))
    if error:
        await interaction.response.send_message(error)
    else:
        await interaction.response.send_message(image_url)

#-----------------------------------------------------------------------------------------------------------------------#

bot.run(TOKEN)
