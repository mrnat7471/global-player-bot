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
        with open('config.json', 'r') as f:
            prefixes = json.load(f)
            prefix = prefixes['prefix']
            version = prefixes['version']

            embed = discord.Embed(
            colour=discord.Colour.blue(),
            description=f"""
            **Version:** {version}
            
                This bot is getting to it's retirement age! Want to stay up to date with all the latest bot features. Please invite our brand new bot [here](https://discord.com/oauth2/authorize?client_id=824979067656863766&permissions=37578816&scope=bot%20applications.commands) and kick our old one.

                **Bot Management:**
                ``{prefix}invite`` - Creates an invite so you can invite this bot to other servers.

                **Reach Radio News:**
                ``{prefix}news`` - Get the latest newspost posted by Reach Radio.
                ``{prefix}latest news`` - Get the latest News From Reach Radio, find out whats happening in the community.

                **Reach Radio:**
                ``{prefix}play`` - Connect to your voice channel and plays Reach Radio.
                ``{prefix}leave`` - Disconnect from Voice Chat in your guild.
                ``{prefix}recentlyplayed`` - Plays 5x most recently played songs on Reach Radio.
                ``{prefix}song`` - Shows current song on Reach Radio.
                ``{prefix}schedule`` - Shows today schedule of presenters.

                **TruckersMP Information:**
                ``{prefix}tmp search`` - Search TruckersMP API for Data by entering StreamID or TMPID.
                ``{prefix}tmp servers`` - Current Status of all TruckersMP Servers
                ``{prefix}tmp traffic (promods, promods arcade, sim1, sim2, arcade, [ats] eusim, [ats] sim)`` - Shows the top busiest place in TruckersMP""",
            title='Reach Radio Public Bot Help!')
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=f'Posted by {ctx.message.author.name}', icon_url=ctx.message.author.avatar_url)

            await ctx.channel.send(embed=embed)
            with open('config.json', 'r') as f:
                logger = json.load(f)
                log = logger['logger']
                for user in log:
                    user = await self.bot.fetch_user(user)
                    await user.send(f"[Help Command] ran by {ctx.message.author.name} ({ctx.message.author.id}) in {ctx.message.author.guild}({ctx.guild.id})")
            print(f"[Help Command] ran by {ctx.message.author.name} ({ctx.message.author.id}) in {ctx.message.author.guild}({ctx.guild.id})")

        await ctx.message.delete()
def setup(bot):
    bot.add_cog(helpCog(bot))
