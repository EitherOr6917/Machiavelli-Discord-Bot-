# Import statements
import random
import discord
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


def setup(client):
    client.add_cog(Games(client))
