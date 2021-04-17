import discord
from discord.ext import commands
import asyncio
import datetime
import json

class leaveCog(commands.Cog):
    def get_prefix(client, message):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes[str(message.guild.id)]
        
    bot = commands.Bot(command_prefix = get_prefix)

    def __init__(self, bot):
        self.bot = bot

    @bot.command(name='leave', aliases=['stop'])
    async def leave(self, ctx):
        try:
            voice = None
            for vc in self.bot.voice_clients:
                if vc.guild == ctx.guild:
                    voice = vc

            if voice == None:
                embed = discord.Embed(colour=discord.Colour.blue(), description="I can't disconnect from a Voice Channel as I am not in a Voice Channel.")
                embed.set_author(name='Global Player', icon_url=self.bot.user.avatar_url)
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_footer(text=f'Global Player Bot', icon_url=self.bot.user.avatar_url)
                await ctx.channel.send(embed=embed)
                return
            VoiceClient = await ctx.voice_client.disconnect()
            bot_channel =  ctx.guild.voice_client

            embed = discord.Embed(colour=discord.Colour.blue(), description="I have disconnected from your voice channel")
            embed.set_author(name='Global Player', icon_url=self.bot.user.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=f'Global Player Bot', icon_url=self.bot.user.avatar_url)
            message = await ctx.channel.send(embed=embed)

            await ctx.message.delete()
            await asyncio.sleep(10)
            await message.delete()
        except Exception as error:
            print(error)

    @leave.error
    async def help_error(self, ctx, error):
        await ctx.message.delete()
        embed = discord.Embed(colour=discord.Colour.red(), title="Error", description=f"""
        Bot has encountered the following error:
        {error}
        
        Common fixes:
        ◉ Make sure that the bot has permission to disconnect it's self.
        """)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Reach Radio Bot', icon_url=self.bot.user.avatar_url)
        await audit.send("<@111893409307860992> & <@510238066829688832>", embed=embed)
        return
        print("\n\n" + str(error) + "\n\n")
def setup(bot):
    bot.add_cog(leaveCog(bot)) 