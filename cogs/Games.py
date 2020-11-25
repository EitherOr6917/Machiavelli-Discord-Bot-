# Import statements
import discord
from discord.ext import commands
import json


# Asynchronous functions
async def do_actions(ctx):
    with open('jsons/duel.json', 'r') as file:
        duel_list = json.load(file)

    player1action = duel_list['Player 1 Action']
    player2action = duel_list['Player 2 Action']

    if player1action == 'attack':
        duel_list['Player 2 HP'] -= 1
    if player2action == 'attack':
        duel_list['Player 1 HP'] -= 1

    player1hp = duel_list['Player 1 HP']
    player2hp = duel_list['Player 2 HP']

    duel_list.pop('Player 1 Action', None)
    duel_list.pop('Player 2 Action', None)

    with open('jsons/duel.json', 'w') as file:
        duel_list = json.load(file)
        json.dump(duel_list, file, indent=4)

    msg = discord.Embed(
        title='Action Phase',
        description=f'Player 1 decided to {player1action}\nPlayer 2 decided to {player2action}\n'
                    f'Player 1 Health: {player1hp}\nPlayer 2 Health: {player2hp}',
        color=discord.Color.purple()
    )
    await ctx.send(embed=msg)


# Synchronous functions
def is_banned(ctx):
    with open('jsons/banned.json', 'r') as file:
        banned_users = json.load(file)

    return str(ctx.author.id) in banned_users


def channel_banned(ctx):
    with open('jsons/bannedChannels.json', 'r') as file:
        banned_channels = json.load(file)

    return str(ctx.channel.id) in banned_channels


def check_actions():
    with open('jsons/duel.json', 'r') as file:
        duel_list = json.load(file)
    return 'Player 1 Action' in duel_list and 'Player 2 Action' in duel_list


class Games(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command(help='Initiates game')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def initiate_duel(self, ctx, target: discord.Member):
        if not is_banned(ctx) and not channel_banned(ctx):
            with open('jsons/duel.json', 'r') as file:
                duel_list = json.load(file)
            if not bool(duel_list):
                duel_list = {'Player 1': str(target.id), 'Player 2': str(ctx.author.id), 'Player 1 HP': 10,
                             'Player 2 HP': 10}

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
                                'cancel_duel to cancel the current game',
                    color=discord.Color.purple()
                )
                await ctx.send(embed=game_in_progress)

    @commands.command(help='Clears lobby for a duel.')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def cancel_duel(self, ctx):
        if not is_banned(ctx) and not channel_banned(ctx):
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
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def duel_attack(self, ctx):
        if not is_banned(ctx) and not channel_banned(ctx):
            with open('jsons/duel.json', 'r') as file:
                duel_list = json.load(file)
            if bool(duel_list) and ((duel_list['Player 1'] == str(ctx.author.id)) or (duel_list['Player 2'] ==
                                                                                      str(ctx.author.id))):
                keys = list(duel_list.keys())
                values = list(duel_list.values())
                player = keys[values.index(str(ctx.author.id))]

                if f'{player} Action' not in duel_list:

                    duel_list[f'{player} Action'] = 'attack'

                    with open('jsons/duel.json', 'w') as file:
                        json.dump(duel_list, file, indent=4)

                    game_created = discord.Embed(
                        description=f'{ctx.author.mention}, your attack has been queued.',
                        color=discord.Color.purple()
                    )
                    await ctx.send(embed=game_created)

                    if check_actions():
                        await do_actions(ctx)
                else:
                    msg = discord.Embed(
                        description=f'{ctx.author.mention} your next action has already been queued.',
                        color=discord.Color.purple()
                    )
                    await ctx.send(embed=msg)
            else:
                game_in_progress = discord.Embed(
                    description=f'{ctx.author.mention} you are not in a game at the moment',
                    color=discord.Color.purple()
                )
                await ctx.send(embed=game_in_progress)


def setup(client):
    client.add_cog(Games(client))
