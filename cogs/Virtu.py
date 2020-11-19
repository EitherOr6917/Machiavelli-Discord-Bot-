# Import statements
import discord
import json
from discord.ext import commands
import random


# Prefixes
def get_prefix(ctx):
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    return prefixes[str(ctx.guild.id)]


# Virtu
def change_virtu(ctx, amount):
    with open('virtuRecord.json', 'r') as file:
        virtu_levels = json.load(file)

    if str(ctx) in virtu_levels:
        if amount < 0:
            virtu_levels[str(ctx)] -= amount
        elif amount > 0:
            virtu_levels[str(ctx)] += amount
        else:
            print('ERROR: Don\'t chance virtu by 0. That is dumb.')
    else:
        virtu_levels[str(ctx)] = 1

        with open('virtuRecord.json', 'w') as file:
            json.dump(virtu_levels, file, indent=4)

    with open('virtuRecord.json', 'w') as file:
        json.dump(virtu_levels, file, indent=4)


def easy_embed(ctx, message):
    embed = discord.Embed(
        description=f'{ctx.author.mention} {message}',
        color=discord.Color.purple()
    )
    return embed


def check_virtu(userid):
    with open('virtuRecord.json', 'r') as file:
        virtu_levels = json.load(file)
        vlevel = virtu_levels[str(userid)]
    return vlevel


class Virtu(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        if message.author != self.client.user:
            change_virtu(message.author.id, 1)

    # Commands
    @commands.command(help='Shows user\'s amount of virtù')
    async def virtu(self, ctx, target: discord.Member = ''):
        citizen = target
        if citizen == '':
            citizen = ctx.author

        with open('virtuRecord.json', 'r') as file:
            virtu_levels = json.load(file)

        if str(citizen.id) not in virtu_levels:
            virtu_levels[str(citizen.id)] = 0

            with open('virtuRecord.json', 'w') as file:
                json.dump(virtu_levels, file, indent=4)

        with open('virtuRecord.json', 'r') as file:
            virtu_levels = json.load(file)
            vlevel = virtu_levels[str(citizen.id)]

            file = discord.File('./images/vLogo.png', filename='vimage.png')
            virtu_msg = discord.Embed(
                title=f'{citizen.nick}\'s Virtù',
                description=f'Virtù Level: {int(vlevel / 100)}\nVirtù total: {vlevel}',
                color=discord.Color.purple()
            )
            virtu_msg.set_thumbnail(url='attachment://vimage.png')

            await ctx.send(file=file, embed=virtu_msg)

    @commands.command(help='Attempts to take virtu from the target')
    async def rob(self, ctx, target: discord.Member, amount: int):
        random.seed()
        robber_savings = check_virtu(ctx.author.id)
        target_savings = check_virtu(target.id)
        if robber_savings >= (2*amount) and target_savings >= amount:
            result = random.randint(0, 2)
            if result == 0:
                change_virtu(ctx.author.id, (-2 * amount))
                change_virtu(target.id, (2 * amount))
                await ctx.send(embed=easy_embed(ctx, 'screwed up the robbery.'))
            else:
                change_virtu(ctx.author.id, amount)
                change_virtu(target.id, (-1 * amount))
                await ctx.send(embed=easy_embed(ctx, 'successfully pulled off the robbery.'))
        else:
            fail_message = discord.Embed(
                description=f'{ctx.author.mention} you don\'t have enough virtù to do this',
                color=discord.Color.purple()
            )

            await ctx.send(embed=fail_message)


def setup(client):
    client.add_cog(Virtu(client))
