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

    @bot.command(name='play', aliases=['join', 'start'])
    async def play(self, ctx, *, message):

        try:
            channel = ctx.author.voice.channel
        except:
            channel = None

        voice = None
        for vc in self.bot.voice_clients:
            if vc.guild == ctx.guild:
                voice = vc

        if channel == None:
            embed = discord.Embed(colour=discord.Colour.blue(), description="You're not in a voice channel")
            embed.set_author(name='Reach Radio', icon_url=self.bot.user.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=f'Reach Radio Bot', icon_url=self.bot.user.avatar_url)
            await ctx.channel.send(embed=embed)
            return
        if voice and voice.is_connected():
            await voice.disconnect()
            VoiceClient = await channel.connect()
        elif voice == channel:
            pass
        else:
            VoiceClient = await channel.connect()
        
        bot_channel =  ctx.guild.voice_client
        r = requests.get("https://bff-web-guacamole.musicradio.com/globalplayer/brands")
        response = r.json()

        message = message.lower()
        station_number = len(response)
        current_number = 0
        playing = False
        for station in response:
            current_number = current_number + 1
            stationname = station['name'].lower()
            if message == stationname:
                playing = True
                station_name = station['name']
                VoiceClient.play(discord.FFmpegPCMAudio(station['streamUrl']))

        if current_number == station_number and playing == False:
            embed = discord.Embed(colour=discord.Colour.blue(), 
            description=f"That station could not be found.")
            embed.set_author(name='Global Player', icon_url=self.bot.user.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=f'Global Player Bot', icon_url=self.bot.user.avatar_url)
            message = await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(colour=discord.Colour.blue(), 
            description=f"Now playing: {station_name}")
            embed.set_author(name='Global Player', icon_url=self.bot.user.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=f'Global Player Bot', icon_url=self.bot.user.avatar_url)
            message = await ctx.channel.send(embed=embed)

        await ctx.message.delete()
        await asyncio.sleep(30)
        await message.delete()

    @play.error
    async def announce_error(self, ctx, error):
        await ctx.message.delete()
        r = requests.get("https://bff-web-guacamole.musicradio.com/globalplayer/brands")
        response = r.json()
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(colour=discord.Colour.blue(), title="Select a Station")
            embed.timestamp = datetime.datetime.utcnow()

            for station in response:
                embed.add_field(name="Station", value=f"{station['name']}", inline=True)

            embed.set_author(name=f'Global Player', icon_url=self.bot.user.avatar_url)
            embed.set_footer(text=f'Global Player Bot', icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
            return

def setup(bot):
    bot.add_cog(reachCog(bot))
