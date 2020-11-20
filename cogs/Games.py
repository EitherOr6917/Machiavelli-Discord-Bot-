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
        with open('jsons/duel.json', 'r') as file:
            duel_list = json.load(file)
        if not bool(duel_list):
            duel_list['Player 1'] = str(target.id)
            duel_list['Player 2'] = str(ctx.author.id)
            duel_list['Player 1 HP'] = 10
            duel_list['Player 2 HP'] = 10

            with open('jsons/duel.json', 'w') as file:
                json.dump(duel_list, file, indent=4)

            game_created = discord.Embed(
                description=f'{ctx.author.mention}, your game has been initiated.',
                color=discord.Color.purple()
            )
            await ctx.send(embed=game_created)
        else:
            game_in_progress = discord.Embed(
                description=f'{ctx.author.mention} there is a game in progress. Use '
                            'clearduel to cancel the current game',
                color=discord.Color.purple()
            )
            await ctx.send(embed=game_in_progress)

    @commands.command(help='Clears lobby for a duel.')
    @commands.guild_only()
    async def cancel_duel(self, ctx):
        with open('jsons/duel.json', 'r') as file:
            duel_list = json.load(file)
        if bool(duel_list):
            duel_list = {}

            with open('jsons/duel.json', 'w') as file:
                json.dump(duel_list, file, indent=4)

            canceled_msg = discord.Embed(
                description=f'{ctx.author.mention} game successfully canceled.',
                color=discord.Color.purple()
            )
            await ctx.send(embed=canceled_msg)
        else:
            no_game_in_progress = discord.Embed(
                description=f'{ctx.author.mention} there is no game to cancel. Use '
                            'initiate to start a new game',
                color=discord.Color.purple()
            )
            await ctx.send(embed=no_game_in_progress)

    @commands.command(help='Queues an attack')
    @commands.guild_only()
    async def duel_attack(self, ctx):
        with open('jsons/duel.json', 'r') as file:
            duel_list = json.load(file)
        if bool(duel_list) and ((duel_list['Player 1'] == str(ctx.author.id)) or (duel_list['Player 2'] ==
                                                                                  str(ctx.author.id))):
            keys = list(duel_list.keys())
            values = list(duel_list.values())
            player = keys[values.index(str(ctx.author.id))]

            duel_list[f'{player} Action'] = 'attack'

            with open('jsons/duel.json', 'w') as file:
                json.dump(duel_list, file, indent=4)

            game_created = discord.Embed(
                description=f'{ctx.author.mention}, your attack has been queued.',
                color=discord.Color.purple()
            )
            await ctx.send(embed=game_created)
        else:
            game_in_progress = discord.Embed(
                description=f'{ctx.author.mention} you are not in a game at the moment',
                color=discord.Color.purple()
            )
            await ctx.send(embed=game_in_progress)


def setup(client):
    client.add_cog(Games(client))
