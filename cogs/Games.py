# Import statements
import random
import discord
import json
from discord.ext import commands


class Games(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command()
    async def bet(self, ctx, *, gamblees):
        win_messages = ['is luckier.', 'wins the bet!', 'has better karma.']
        gamblers = gamblees.split()
        gambler_winner = random.choice(gamblers)

        gambler_message = discord.Embed(
            description=f'{gambler_winner} {random.choice(win_messages)}',
            color=discord.Color.purple()
        )
        await ctx.send(embed=gambler_message)

    @commands.command()
    async def startgame(self, ctx):
        players_q = discord.Embed(
            description=f'{ctx.author.mention} specify number of players with setplayercount',
            color=discord.Color.purple()
        )


def setup(client):
    client.add_cog(Games(client))
