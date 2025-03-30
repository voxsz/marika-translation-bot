import discord
import requests
import re
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DEEPL_API_KEY = os.getenv('DEEPL_API_KEY')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"

def detect_language(text):
    # 日本語文字が含まれていれば「JA」、それ以外は「EN」
    if re.search(r'[\u3040-\u30ff\u4e00-\u9fff]', text):
        return 'JA'
    else:
        return 'EN'

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')

@client.event
async def on_message(message):
    # 自分自身 or 他Botのメッセージは無視
    if message.author == client.user or message.author.bot:
        return

    source_lang = detect_language(message.content)
    target_lang = 'EN' if source_lang == 'JA' else 'JA'

    data = {
        'auth_key': DEEPL_API_KEY,
        'text': message.content,
        'target_lang': target_lang
    }

    response = requests.post(DEEPL_API_URL, data=data)

    if response.status_code == 200:
        translated_text = response.json()['translations'][0]['text']
        await message.channel.send(f'🌐 翻訳 ({source_lang}→{target_lang}): {translated_text}')
    else:
        await message.channel.send('⚠️ 翻訳エラーが発生しました')

client.run(DISCORD_TOKEN)
