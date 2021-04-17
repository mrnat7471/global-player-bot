import discord
from discord.ext import commands, tasks
import datetime
import ffmpeg
import json
import requests
import time
from itertools import cycle
import os
from os import listdir
from os.path import isfile, join
import logging
import asyncio
from discord.ext.commands import AutoShardedBot, CommandNotFound

def get_prefix(client, message):
        with open('config.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes['prefix']

bot = AutoShardedBot(command_prefix=get_prefix, pm_help=True, fetch_offline_members=False)
bot.remove_command('help')

@bot.event
async def on_ready():
    print("Bot has been started")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="g!help | Global Stations"))
    await asyncio.sleep(15)
    change_status.start()

@tasks.loop(seconds=255)
async def change_status():
    r = requests.get("https://bff-web-guacamole.musicradio.com/globalplayer/brands")
    response = r.json()
    for station in response:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{station['name']}"))
        await asyncio.sleep(15)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

cogs_dir = "cogs"

if __name__ == '__main__':
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
        except (discord.ClientException, ModuleNotFoundError):
            print(f'Failed to load extension {extension}.')

while True:
    try:
        with open('config.json', 'r') as f:
            timez = json.load(f)
            tokentxt = timez['token']
        bot.loop.run_until_complete(bot.run(tokentxt))
    except BaseException:
        pass
