# Import statements
import discord
from discord.ext import commands
import json


# Functions
def is_banned(ctx):
    with open('jsons/banned.json', 'r') as file:
        banned_users = json.load(file)

    return str(ctx.author.id) in banned_users


def channel_banned(ctx):
    with open('jsons/bannedChannels.json', 'r') as file:
        banned_channels = json.load(file)

    return str(ctx.channel.id) in banned_channels


class Cute(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command(help='Rickrolls the voicechat you are in')
    @commands.guild_only()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def rickroll(self, ctx):
        if not is_banned(ctx) and not channel_banned(ctx):
            channel = ctx.author.voice.channel
            voice = await channel.connect()
            await voice.connect()

            dumb = discord.Embed(
                description='Get rickrolled lmao',
                color=discord.Color.purple()
            )
            await ctx.send(embed=dumb)


def setup(client):
    client.add_cog(Cute(client))
