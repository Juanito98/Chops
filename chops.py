import discord
import random
import asyncio
import os
from discord.ext import commands

bot = discord.Client()

bot = commands.Bot(command_prefix='-chops ')

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