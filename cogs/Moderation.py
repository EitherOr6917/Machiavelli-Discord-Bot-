# Import statements
import discord
from discord.ext import commands


class Moderator(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        # do some extra stuff here
        if self.client.user.mentioned_in(message):
            reply_message = discord.Embed(
                description=f'{message.author.mention} please use command >help for more information on my commands.',
                color=discord.Color.purple()
            )
            await message.channel.send(embed=reply_message)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as: {self.client.user}\nDiscord version: {discord.__version__}\n')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            error_message1 = discord.Embed(
                description=f'{ctx.author.mention} please pass in the missing required arguments.',
                color=discord.Color.purple()
            )
            await ctx.send(embed=error_message1)
        if isinstance(error, commands.CommandNotFound):
            error_message2 = discord.Embed(
                description=f'{ctx.author.mention} that command does not exist.',
                color=discord.Color.purple()
            )
            await ctx.send(embed=error_message2)

    # Commands
    @commands.command()
    async def ping(self, ctx):
        ping_message = discord.Embed(
            description=f'Latency: {"{:.1f}".format(self.client.latency * 1000)}ms.',
            color=discord.Color.purple()
        )
        await ctx.send(embed=ping_message)

    @commands.command()
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1)

        cleared_message = discord.Embed(
            description=f'Cleared {amount} messages.',
            color=discord.Color.purple()
        )
        await ctx.send(embed=cleared_message)

    @commands.command(aliases=['dm'])
    @commands.has_permissions(administrator=True)
    async def direct_message(self, ctx, messagee: discord.Member, *, message):
        dm_sent = discord.Embed(
            description=f':upside_down: {ctx.author.mention} sent!',
            color=discord.Color.purple()
        )
        await messagee.send(message)
        await ctx.send(embed=dm_sent)

    @commands.command()
    async def github(self, ctx):
        github_message = discord.Embed(
            description=f'My code is on Github here: https://github.com/EitherOr6917/eitherBot.py',
            color=discord.Color.purple()
        )
        await ctx.send(embed=github_message)


def setup(client):
    client.add_cog(Moderator(client))
