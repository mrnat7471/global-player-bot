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

    @bot.command(name='catchup')
    async def catchup(self, ctx, *, message):
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

        presenterdict = {}
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
                station_name = station['name']
                j = requests.get(f"https://bff-web-guacamole.musicradio.com/globalplayer/catchups/{station['brandSlug']}/uk")
                response2 = j.json()
                presenter_number = len(response2)

                embed = discord.Embed(colour=discord.Colour.blue(), title=f"Select a {station['name']} Presenter")
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_thumbnail(url=station['brandLogo'])
                presenter_number = 1
                for presenter in response2:
                    presenter_number = presenter_number + 1
                    if presenter_number == 11:
                        break
                    else:
                        number = presenter_number
                        if number == 2:
                            emoji = "1️⃣"
                            presenterdict[number] = presenter['id']
                        elif number == 3:
                            emoji = "2️⃣"
                            presenterdict[number] = presenter['id']
                        elif number == 4:
                            emoji = "3️⃣"
                            presenterdict[number] = presenter['id']
                        elif number == 5:
                            emoji = "4️⃣"
                            presenterdict[number] = presenter['id']
                        elif number == 6:
                            emoji = "5️⃣"
                            presenterdict[number] = presenter['id']
                        elif number == 7:
                            emoji = "6️⃣"
                            presenterdict[number] = presenter['id']
                        elif number == 8:
                            emoji = "7️⃣"
                            presenterdict[number] = presenter['id']
                        elif number == 9:
                            emoji = "8️⃣"
                            presenterdict[number] = presenter['id']
                        elif number == 10:
                            emoji = "9️⃣"
                            presenterdict[number] = presenter['id']
                        embed.add_field(name=f"Presenter {emoji}", value=f"{presenter['title']}", inline=False)
                        
                embed.set_author(name=f'Global Player', icon_url=self.bot.user.avatar_url)
                embed.set_footer(text=f'Global Player Bot', icon_url=self.bot.user.avatar_url)
                message = await ctx.send(embed=embed)
                await message.add_reaction("▶️")
                for number in range(1, presenter_number+1):
                    if number == 1:
                        await message.add_reaction("1️⃣")
                    elif number == 2:
                        await message.add_reaction("2️⃣")
                    elif number == 3:
                        await message.add_reaction("3️⃣")
                    elif number == 4:
                        await message.add_reaction("4️⃣")
                    elif number == 5:
                        await message.add_reaction("5️⃣")
                    elif number == 6:
                        await message.add_reaction("6️⃣")
                    elif number == 7:
                        await message.add_reaction("7️⃣")
                    elif number == 8:
                        await message.add_reaction("8️⃣")
                    elif number == 9:
                        await message.add_reaction("9️⃣")


                def check(reaction, user):
                    global cachedEmoji
                    cachedEmoji = str(reaction.emoji)
                    return str(reaction.emoji) ==  "1️⃣" or str(reaction.emoji) ==  "2️⃣" or str(reaction.emoji) ==  "3️⃣" or str(reaction.emoji) ==  "4️⃣" or str(reaction.emoji) ==  "5️⃣" or str(reaction.emoji) ==  "6️⃣" or str(reaction.emoji) ==  "7️⃣" or str(reaction.emoji) ==  "8️⃣" or str(reaction.emoji) ==  "9️⃣" or str(reaction.emoji) ==  "▶️"
                await asyncio.sleep(2)
                await self.bot.wait_for('reaction_add', check=check)
                print("REACTION DETECTED")

                if cachedEmoji == "1️⃣":
                    showid = presenterdict[2]
                elif cachedEmoji == "2️⃣":
                    showid = presenterdict[3]
                elif cachedEmoji == "3️⃣":
                    showid = presenterdict[4]
                elif cachedEmoji == "4️⃣":
                    showid = presenterdict[5]
                elif cachedEmoji == "5️⃣":
                    showid = presenterdict[6]
                elif cachedEmoji == "6️⃣":
                    showid = presenterdict[7]
                elif cachedEmoji == "7️⃣":
                    showid = presenterdict[8]
                elif cachedEmoji == "8️⃣":   
                    showid = presenterdict[9]
                elif cachedEmoji == "9️⃣":
                    showid = presenterdict[10]
                else:
                    showid = None

                if cachedEmoji == "▶️":
                    presenterdict = {}
                    station_name = station['name']
                    j = requests.get(f"https://bff-web-guacamole.musicradio.com/globalplayer/catchups/{station['brandSlug']}/uk")
                    response2 = j.json()
                    presenter_number = len(response2)

                    embed = discord.Embed(colour=discord.Colour.blue(), title=f"Select a {station['name']} Presenter")
                    embed.timestamp = datetime.datetime.utcnow()
                    presenter_number = 0
                    for presenter in response2:
                        presenter_number = presenter_number + 1
                        if presenter_number >= 11:
                            number = presenter_number
                            if number == 11:
                                emoji = "1️⃣"
                                presenterdict[number] = presenter['id']
                            elif number == 12:
                                emoji = "2️⃣"
                                presenterdict[number] = presenter['id']
                            elif number == 13:
                                emoji = "3️⃣"
                                presenterdict[number] = presenter['id']
                            elif number == 14:
                                emoji = "4️⃣"
                                presenterdict[number] = presenter['id']
                            elif number == 15:
                                emoji = "5️⃣"
                                presenterdict[number] = presenter['id']
                            elif number == 16:
                                emoji = "6️⃣"
                                presenterdict[number] = presenter['id']
                            elif number == 17:
                                emoji = "7️⃣"
                                presenterdict[number] = presenter['id']
                            elif number == 18:
                                emoji = "8️⃣"
                                presenterdict[number] = presenter['id']
                            elif number == 19:
                                emoji = "9️⃣"
                                presenterdict[number] = presenter['id']
                            embed.add_field(name=f"Presenter {emoji}", value=f"{presenter['title']}", inline=False)
                    embed.set_author(name=f'Global Player', icon_url=self.bot.user.avatar_url)
                    embed.set_footer(text=f'Global Player Bot', icon_url=self.bot.user.avatar_url)
                    message = await ctx.send(embed=embed)
                    for number in range(11, presenter_number+1):
                        if number == 11:
                            await message.add_reaction("1️⃣")
                        elif number == 12:
                            await message.add_reaction("2️⃣")
                        elif number == 13:
                            await message.add_reaction("3️⃣")
                        elif number == 14:
                            await message.add_reaction("4️⃣")
                        elif number == 15:
                            await message.add_reaction("5️⃣")
                        elif number == 16:
                            await message.add_reaction("6️⃣")
                        elif number == 17:
                            await message.add_reaction("7️⃣")
                        elif number == 18:
                            await message.add_reaction("8️⃣")
                        elif number == 19:
                            await message.add_reaction("9️⃣")

                    def check(reaction, user):
                        global cachedEmoji
                        cachedEmoji = str(reaction.emoji)
                        return str(reaction.emoji) ==  "1️⃣" or str(reaction.emoji) ==  "2️⃣" or str(reaction.emoji) ==  "3️⃣" or str(reaction.emoji) ==  "4️⃣" or str(reaction.emoji) ==  "5️⃣" or str(reaction.emoji) ==  "6️⃣" or str(reaction.emoji) ==  "7️⃣" or str(reaction.emoji) ==  "8️⃣" or str(reaction.emoji) ==  "9️⃣" or str(reaction.emoji) ==  "▶️"
                    await asyncio.sleep(2)
                    await self.bot.wait_for('reaction_add', check=check)
                    print("REACTION DETECTED")

                    if cachedEmoji == "1️⃣":
                        showid = presenterdict[11]
                    elif cachedEmoji == "2️⃣":
                        showid = presenterdict[12]
                    elif cachedEmoji == "3️⃣":
                        showid = presenterdict[13]
                    elif cachedEmoji == "4️⃣":
                        showid = presenterdict[14]
                    elif cachedEmoji == "5️⃣":
                        showid = presenterdict[15]
                    elif cachedEmoji == "6️⃣":
                        showid = presenterdict[16]
                    elif cachedEmoji == "7️⃣":
                        showid = presenterdict[16]
                    elif cachedEmoji == "8️⃣":   
                        showid = presenterdict[17]
                    elif cachedEmoji == "9️⃣":
                        showid = presenterdict[18]
                    else:
                        showid = None
                #VoiceClient.play(discord.FFmpegPCMAudio(station['streamUrl']))

        j = requests.get(f"https://bff-web-guacamole.musicradio.com/globalplayer/catchups/{showid}")
        response2 = j.json()
        presenter_number = len(response2)

        embed = discord.Embed(colour=discord.Colour.blue(), title=f"Select a program.")
        embed.timestamp = datetime.datetime.utcnow()
        number = 0
        presenterdict = {}
        for presenter in response2['episodes']:
            number = number + 1
            if number == 1:
                emoji = "1️⃣"
                presenterdict[number] = presenter['streamUrl']
            elif number == 2:
                emoji = "2️⃣"
                presenterdict[number] = presenter['streamUrl']
            elif number == 3:
                emoji = "3️⃣"
                presenterdict[number] = presenter['streamUrl']
            elif number == 4:
                emoji = "4️⃣"
                presenterdict[number] = presenter['streamUrl']
            elif number == 5:
                emoji = "5️⃣"
                presenterdict[number] = presenter['streamUrl']
            elif number == 6:
                emoji = "6️⃣"
                presenterdict[number] = presenter['streamUrl']
            elif number == 7:
                emoji = "7️⃣"
                presenterdict[number] = presenter['streamUrl']
            elif number == 8:
                emoji = "8️⃣"
                presenterdict[number] = presenter['streamUrl']
            elif number == 9:
                emoji = "9️⃣"
                presenterdict[number] = presenter['streamUrl']

        
            d1 = datetime.datetime.strptime(str(presenter['startDate']),"%Y-%m-%dT%H:%M:%S+00:00")
            date = d1.strftime("%d/%m/%y")
            embed.add_field(name=f"{presenter['title']} {date} - {emoji}", value=f"{presenter['description']}", inline=False)
        
        embed.set_author(name=f'Global Player', icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=f'Global Player Bot', icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url=presenter['imageUrl'])
        message = await ctx.send(embed=embed)

        for number in range(0, number+1):
            if number == 1:
                await message.add_reaction("1️⃣")
            elif number == 2:
                await message.add_reaction("2️⃣")
            elif number == 3:
                await message.add_reaction("3️⃣")
            elif number == 4:
                await message.add_reaction("4️⃣")
            elif number == 5:
                await message.add_reaction("5️⃣")
            elif number == 6:
                await message.add_reaction("6️⃣")
            elif number == 7:
                await message.add_reaction("7️⃣")
            elif number == 8:
                await message.add_reaction("8️⃣")
            elif number == 9:
                await message.add_reaction("9️⃣")

        def check(reaction, user):
            global cachedEmoji
            cachedEmoji = str(reaction.emoji)
            return str(reaction.emoji) ==  "1️⃣" or str(reaction.emoji) ==  "2️⃣" or str(reaction.emoji) ==  "3️⃣" or str(reaction.emoji) ==  "4️⃣" or str(reaction.emoji) ==  "5️⃣" or str(reaction.emoji) ==  "6️⃣" or str(reaction.emoji) ==  "7️⃣" or str(reaction.emoji) ==  "8️⃣" or str(reaction.emoji) ==  "9️⃣" or str(reaction.emoji) ==  "▶️"
        await asyncio.sleep(2)
        await self.bot.wait_for('reaction_add', check=check)
        print("REACTION DETECTED")

        if cachedEmoji == "1️⃣":
            showid = presenterdict[1]
        elif cachedEmoji == "2️⃣":
            showid = presenterdict[2]
        elif cachedEmoji == "3️⃣":
            showid = presenterdict[3]
        elif cachedEmoji == "4️⃣":
            showid = presenterdict[4]
        elif cachedEmoji == "5️⃣":
            showid = presenterdict[5]
        elif cachedEmoji == "6️⃣":
            showid = presenterdict[6]
        elif cachedEmoji == "7️⃣":
            showid = presenterdict[6]
        elif cachedEmoji == "8️⃣":   
            showid = presenterdict[7]
        elif cachedEmoji == "9️⃣":
            showid = presenterdict[8]
        else:
            showid = None

        VoiceClient.play(discord.FFmpegPCMAudio(showid))

    @catchup.error
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
