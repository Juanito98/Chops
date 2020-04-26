import discord
import random
import asyncio
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = discord.Client()

bot = commands.Bot(command_prefix='-chops ')

@bot.command(name='foto')
async def foto(ctx):
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
async def saluda(ctx):
    saludos = [
        'Hola prro! :dog:',
        'Kyc y deme comida :canned_food:',
        'Tú no me mandas :angry:'
    ]
    response = random.choice(saludos)
    await ctx.send(response)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(os.environ['DISCORD_TOKEN'])