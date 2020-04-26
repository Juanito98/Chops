import discord
import random
import asyncio
from discord.ext import commands

bot = discord.Client()

bot = commands.Bot(command_prefix='-chops ')

@bot.command(name='saluda')
async def saluda(ctx):
    await ctx.send("Hola prro")


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run('NzA0MDU0MDM3MTQxNjUxNTY2.XqXjeQ.Xjek8c2kUVD-TKbPfdL5YFzSYMo')