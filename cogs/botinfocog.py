import discord
from discord.ext import commands
import asyncio
import datetime
import time
import platform
import json
import requests

start_time = time.time()

class botinfoCog(commands.Cog):
    def get_prefix(client, message):
        with open('config.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes['prefix']

    bot = commands.Bot(command_prefix = get_prefix)

    def __init__(self, bot):
        self.bot = bot

    @bot.command(name='botinfo')
    async def botinfo(self, ctx):
        ms = self.bot.latency * 1000
        current_time = time.time()
        difference = int(round(current_time - start_time))
        uptime = str(datetime.timedelta(seconds=difference))
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__

        i = 0
        for guild in self.bot.guilds:
            i = i + guild.member_count

        memberCount = i

        i = 0
        for vc in self.bot.voice_clients:
            members = len(vc.channel.members)
            i = i + members 
        print("Bot Listeners: ",i)

        try:
            r = requests.get("https://media-ssl.musicradio.com/status-json.xsl")
            response = r.json()
            channels = response['icestats']['source']
            for channel in channels:
                i = i + channel['listeners']

            print("All Listeners: ", i)
        except:
            pass



        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name='Global Player Bot Information', icon_url=self.bot.user.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Global Player', icon_url=self.bot.user.avatar_url)

        embed.add_field(name="Python Version", value=f"{pythonVersion}", inline=True)
        embed.add_field(name="Discord PY Version", value=f"{dpyVersion}", inline=True)
        embed.add_field(name="Uptime", value=uptime, inline=True)
        embed.add_field(name="Members", value=memberCount, inline=True)
        embed.add_field(name="Listeners", value=i, inline=True)
        embed.add_field(name="Ping:", value='Pong! {0}ms'.format(round(ms)), inline=True)
        embed.add_field(name="Coded by", value="Nathan7471#7471", inline=True)

        t = await ctx.channel.send(embed=embed)

        await ctx.message.delete()
def setup(bot):
    bot.add_cog(botinfoCog(bot))
