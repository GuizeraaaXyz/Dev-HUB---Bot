import discord
from discord.ext import commands, tasks
import feedparser
from translate import Translator
import time
import os
from dotenv import load_dotenv  # TEM QUE IMPORTAR ISSO PRA CARREGAR O .env

load_dotenv()  # CARREGA O .env, SEM ISSO N TEM TOKEN
TOKEN = os.getenv("TOKEN")

CHANNEL_ID = 1374499222224900106
RSS_FEED = 'https://www.theverge.com/rss/index.xml'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

ult_data = 0  # pra não repetir notícia

def traduzir(texto):
    tradutor = Translator(to_lang="pt")
    try:
        return tradutor.translate(texto)
    except:
        return texto

@bot.event
async def on_ready():
    print(f'bot {bot.user} ta on mlk 😎')
    buscar_noticia.start()

@tasks.loop(minutes=60)  # roda a cada 1h pra news fresh
async def buscar_noticia():
    global ult_data
    feed = feedparser.parse(RSS_FEED)
    if feed.entries:
        entry = feed.entries[0]
        pub_time = time.mktime(entry.published_parsed)

        if pub_time > ult_data:
            ult_data = pub_time
            canal = bot.get_channel(CHANNEL_ID)
            titulo_traduzido = traduzir(entry.title)
            await canal.send(f'📢 **Notícia tech nova!**\n**{titulo_traduzido}**\n{entry.link}')

@bot.command()
async def noticia(ctx):
    feed = feedparser.parse(RSS_FEED)
    if feed.entries:
        entry = feed.entries[0]
        titulo_traduzido = traduzir(entry.title)
        await ctx.send(f'🧠 tech news do momento:\n**{titulo_traduzido}**\n{entry.link}')

bot.run(TOKEN)
