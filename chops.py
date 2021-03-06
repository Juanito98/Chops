import discord
import random
import asyncio
import os
import giphy_client
import json
import numpy
from discord.ext import commands
from dotenv import load_dotenv
from giphy_client.rest import ApiException
import matplotlib.pyplot as plt
from math import exp, sin, cos, pi, log as ln


config = json.load(open('config.json'))

# Get credentials
load_dotenv()
discord_token = os.environ['DISCORD_TOKEN']
giphy_token = os.environ['GIPHY_TOKEN']

# Define instances
bot = commands.Bot(command_prefix=commands.when_mentioned_or('-chops ', '-'))
giphy_api_instance = giphy_client.DefaultApi()

@bot.command(name='volado')
async def tossUpCmd(ctx):
    await ctx.send(random.choice(["Águila", "Sol"]))

def get_plot(msg):
    t = numpy.linspace(-10, 10, num=100)
    y = eval('[{} for x in t]'.format(msg))
    plt.plot(t, y)
    plt.ylabel('f(x) = {}'.format(msg))
    plt.xlabel('x')
    plt.title('Gráfica')
    filename = 'random_plot.png'
    filepath = 'tmp/random_plot.png'
    plt.savefig(filepath)
    plt.close()
    File = discord.File(filepath, filename)
    return File

@bot.command(name='plot')
async def plotCmd(ctx, *, msg="sin(x)"):
    file = get_plot(msg)
    await ctx.send("", file=file)

def random_gif():
    response = giphy_api_instance.gifs_random_get(giphy_token)
    gif = response.data
    return gif.url

def search_gifs(query):
    try:
        return giphy_api_instance.gifs_search_get(giphy_token, query, limit=8, rating='g')
    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e

def gif_response(emotion):
    gifs = search_gifs(emotion)
    lst = list(gifs.data)
    gif = random.choices(lst)
    return gif[0].url

@bot.command(name='gif')
async def gifCmd(ctx, *, msg=""):
    if msg == "":
        gif = random_gif()
    else:
        gif = gif_response(msg)
    await ctx.send(gif)

@bot.command(name='foto')
async def photoCmd(ctx):
    meta = random.choice(config['photos'])
    msg = random.choice(config['frases'])
    file = discord.File(meta['filepath'], meta['filename'])

    await ctx.message.add_reaction(config['emoji']['camera'])
    await ctx.send(msg, file=file)

@bot.command(name='saluda')
async def hiCmd(ctx):
    sender = ctx.author.name
    saludo = random.choice(config["greetings"]).format(sender)

    await ctx.send(saludo)
    await ctx.send(gif_response(saludo))


@bot.command(name='kick')
async def kickCmd(ctx, *, member : discord.Member):
    await member.kick()
    await ctx.send(gif_response('kick'))

@bot.event
async def on_message(message):
    if "te amo" in message.content.lower():
        await message.add_reaction(config['emoji']['heart'])
    if "chops" in message.content.lower():
        await message.add_reaction(config['emoji']['chops'])

    await bot.process_commands(message)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(discord_token)
