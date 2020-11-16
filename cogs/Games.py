# Import statements
import random
import discord
from discord.ext import commands
import json


# Prefixes
def get_prefix(ctx):
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    return prefixes[str(ctx.guild.id)]


class Games(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        if message.content.startswith(get_prefix(message)):
            with open('virtu.json', 'r') as file:
                virtu_levels = json.load(file)

            if message.author.id not in virtu_levels:
                virtu_levels[str(message.author.id)] += 1

            with open('virtu.json', 'w') as file:
                json.dump(virtu_levels, file, indent=4)

    # Commands
    @commands.command(help='Decides which of the given options wins')
    async def bet(self, ctx, *, gamblees):
        gamblers = gamblees.split()
        gambler_winner = random.choice(gamblers)

        gambler_message = discord.Embed(
            description=f'{gambler_winner} wins.',
            color=discord.Color.purple()
        )
        await ctx.send(embed=gambler_message)

    @commands.command(help='Currently non functional command')
    async def startgame(self, ctx):
        players_q = discord.Embed(
            description=f'{ctx.author.mention} specify number of players with setplayercount',
            color=discord.Color.purple()
        )

        await ctx.send(embed=players_q)

    @commands.command(help='Shows user\'s amount of virtù')
    async def virtu(self, ctx):
        with open('virtu.json', 'r') as file:
            virtu_levels = json.load(file)

        if ctx.author.id not in virtu_levels:
            virtu_levels[str(ctx.author.id)] = 0

            with open('virtu.json', 'w') as file:
                json.dump(virtu_levels, file, indent=4)

        with open('virtu.json', 'r') as file:
            virtu_levels = json.load(file)

            virtu_msg = discord.Embed(
                description=f'{ctx.author.mention}, your virtù is {virtu_levels[str(ctx.author.id)]}',
                color=discord.Color.purple()
            )

            await ctx.send(embed=virtu_msg)


def setup(client):
    client.add_cog(Games(client))
