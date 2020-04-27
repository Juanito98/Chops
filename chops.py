import discord
import random
import asyncio
import os
import giphy_client
from discord.ext import commands
from dotenv import load_dotenv
from giphy_client.rest import ApiException

load_dotenv()
discord_token = os.environ['DISCORD_TOKEN']
giphy_token = os.environ['GIPHY_TOKEN']

bot = discord.Client()
giphy_api_instance = giphy_client.DefaultApi()

bot = commands.Bot(command_prefix='-chops ')

def search_gifs(query):
    try:
        return giphy_api_instance.gifs_search_get(giphy_token, query, limit=5, rating = 'g')
    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e

def random_gif():
    response = giphy_api_instance.gifs_random_get(giphy_token)
    gif = response.data
    return gif.url

def gif_response(emotion):
    gifs = search_gifs(emotion)
    lst = list(gifs.data)
    gif = random.choices(lst)
    return gif[0].url

@bot.command(name='gif')
async def gifCmd(ctx, msg=""):
    if msg == "":
        gif = random_gif()
    else:
        gif = gif_response(msg)
    await ctx.send(gif)

@bot.command(name='foto')
async def fotoCmd(ctx):
    files = [
        'chops1.jpeg',
        'chops2.jpeg',
        'chops3.jpeg'
    ]
    mensajes = [
        'Ten :3',
        'Te quiero :heart:',
        ''
    ]
    filename = random.choice(files)
    msg = random.choice(mensajes)
    filepath = "Resources/"+filename
    file = discord.File(filepath, filename)
    await ctx.send(msg, file=file)

@bot.command(name='saluda')
async def saludaCmd(ctx):
    saludos = [
        'Hola prro! :dog:',
        'Kyc y deme comida :canned_food:',
        'Tú no me mandas :angry:',
    ]
    saludo = random.choice(saludos)
    await ctx.send(saludo)
    await ctx.send(gif_response(saludo))


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(discord_token)