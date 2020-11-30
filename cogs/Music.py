# Import statements
import asyncio
import discord
import youtube_dl
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


# Music bot stuff from Rapptz discord example
youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'music/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command(help='Connects to specified voice channel')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def connect(self, ctx):
        if not is_banned(ctx) and not channel_banned(ctx):
            if ctx.voice_client is not None:
                return await ctx.voice_client.move_to(ctx.author.voice.channel)

            await ctx.author.voice.channel.connect()

    @commands.command(help='Connects to specified voice channel')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def disconnect(self, ctx):
        if not is_banned(ctx) and not channel_banned(ctx):
            await ctx.voice_client.disconnect()

    # @commands.command(help='Plays audio from youtube link')
    # @commands.guild_only()
    # @commands.cooldown(1, 2, commands.BucketType.user)
    # async def play(self, ctx, *, url):
    #     if not is_banned(ctx) and not channel_banned(ctx):
    #         async with ctx.typing():
    #             player = await YTDLSource.from_url(url, loop=self.client.loop)
    #             ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    #
    # #         await ctx.send(f'Now playing {player.title}')
    #
    # @commands.command(help='Changes the volume of the bot')
    # @commands.guild_only()
    # @commands.cooldown(1, 1, commands.BucketType.user)
    # async def volume(self, ctx, volume: int):
    #     if not is_banned(ctx) and not channel_banned(ctx):
    #         ctx.voice_client.source.volume = volume / 100
    #         await ctx.send(f'Changed volume to {volume}%')


def setup(client):
    client.add_cog(Music(client))
