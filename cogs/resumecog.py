import discord
from discord.ext import commands, tasks
from discord.ext.commands import AutoShardedBot
import asyncio
import datetime
import ffmpeg
import json
import requests
import time
from itertools import cycle
import os
from os import listdir
from os.path import isfile, join
import sys, traceback
import logging

class reachCog(commands.Cog):
    def get_prefix(client, message):
        with open('config.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes['prefix']

    bot = commands.Bot(command_prefix = get_prefix)


    def __init__(self, bot):
        self.bot = bot

    @bot.command(name='resume')
    async def play(self, ctx):
        voice = None
        for vc in self.bot.voice_clients:
            if vc.guild == ctx.guild:
                voice = vc

        if voice.is_paused():
            ctx.voice_client.resume()
        else:
            pass

        embed = discord.Embed(colour=discord.Colour.blue(), description=f"Continueing to play.")
        embed.set_author(name='Global Player', icon_url=self.bot.user.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Global Player Bot', icon_url=self.bot.user.avatar_url)
        message = await ctx.channel.send(embed=embed)
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(reachCog(bot))
