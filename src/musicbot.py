import discord
import os
from discord.ext import commands

bot = commands.Bot(command_prefix=".")

def read_token():
    with open('Token.txt', "r") as file:
        lines = file.readlines()
        return lines[0].strip()


token = read_token()

@bot.event
async def on_ready():
  print(f'{bot.user} has logged in.')
  bot.load_extension('cogs.music')

bot.run(token)
