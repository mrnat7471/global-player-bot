import discord
from discord.ext import commands
import asyncio
import datetime
import json

class helpCog(commands.Cog):
    def get_prefix(client, message):
        with open('config.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes['prefix']

    bot = commands.Bot(command_prefix = get_prefix)
    bot.remove_command('help')

    def __init__(self, bot):
        self.bot = bot

    @bot.command(name='help')
    async def help(self, ctx):
        embed = discord.Embed(colour=discord.Colour.blue(), description=f"""
        **Help Command:**

        Prefix: ``g!``

        g!play - Lists all stations available from global player
        g!play <station> - Plays selected station
        g!leave - Disconnects bot from voice channel
        g!catchup - Lists all stations available from global player
        g!catchup <station> - Lists all presenters and their catchup shows available to listen to.
        g!queue <station> - Add a catchup show to the queue
        g!thequeue - Check the amount in the queue
        g!pause - Pause audio.
        g!resume - Resume audio.
        """)
        embed.set_author(name='Global Player', icon_url=self.bot.user.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Global Player Bot', icon_url=self.bot.user.avatar_url)
        message = await ctx.channel.send(embed=embed)

        await ctx.message.delete()
def setup(bot):
    bot.add_cog(helpCog(bot))
