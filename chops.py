import discord
import random
import asyncio
import os
import giphy_client
import json
from discord.ext import commands
from dotenv import load_dotenv
from giphy_client.rest import ApiException

config = json.load(open('config.json'))

# Get credentials
load_dotenv()
discord_token = os.environ['DISCORD_TOKEN']
giphy_token = os.environ['GIPHY_TOKEN']

# Define instances
bot = commands.Bot(command_prefix='-chops ')
giphy_api_instance = giphy_client.DefaultApi()

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
    print(msg)
    if msg == "":
        gif = random_gif()
    else:
        gif = gif_response(msg)
    await ctx.send(gif)

@bot.command(name='foto')
async def photoCmd(ctx):
    meta = random.choice(config['photos'])
    msg = random.choice(config['messages'])
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
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(discord_token)
