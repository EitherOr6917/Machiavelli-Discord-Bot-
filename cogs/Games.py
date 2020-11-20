# Import statements
import discord
from discord.ext import commands
import json


class Games(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command(help='Initiates game')
    @commands.guild_only()
    async def initiate(self, ctx, target: discord.Member):
        with open('duel.json', 'r') as file:
            duel_list = json.load(file)
        if not duel_list:
            duel_list['Player 1'] = str(target.id)
            duel_list['Player 2'] = str(ctx.author.id)
            duel_list['Player 1 HP'] = 10
            duel_list['Player 2 HP'] = 10

            with open('duel.json', 'w') as file:
                json.dump(duel_list, file, indent=4)

            game_created = discord.Embed(
                description=f'{ctx.author.mention}, your game has been initiated.',
                color=discord.Color.purple()
            )
            await ctx.send(embed=game_created)
        else:
            game_in_progress = discord.Embed(
                description=f'{ctx.author.mention} there is a game in progress. Use {self.client.cmmand_prefix}'
                            'clearduel to cancel the current game',
                color=discord.Color.purple()
            )
            await ctx.send(embed=game_in_progress)

    @commands.command(help='Clears lobby for a duel.')
    @commands.guild_only()
    async def cancelduel(self, ctx):
        with open('duel.json', 'r') as file:
            duel_list = json.load(file)
        if duel_list:
            with open('duel.json', 'w') as file:
                json.dump(duel_list, file, indent=4)

            canceled_msg = discord.Embed(
                description=f'{ctx.author.mention} game successfully canceled.',
                color=discord.Color.purple()
            )
            await ctx.send(embed=canceled_msg)
        else:
            no_game_in_progress = discord.Embed(
                description=f'{ctx.author.mention} there is no game to cancel. Use {self.client.cmmand_prefix}'
                            'initiate to start a new game',
                color=discord.Color.purple()
            )
            await ctx.send(embed=no_game_in_progress)


def setup(client):
    client.add_cog(Games(client))
