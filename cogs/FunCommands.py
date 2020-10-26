# Import statements
import discord
import random
from discord.ext import commands


class FunCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command()
    async def kill(self, ctx, target: discord.Member):
        self_kill_messages = ['decided to off themselves.', 'decided the donuts weren\'t good enough.',
                              'wants to try making toast in a bath',
                              'decides to become a ceiling fixture.']
        kill_messages = ['shoots', 'plants bomb and explodes', 'runs over', 'contracts Jon Doe to kill']

        if target == ctx.author:
            kill_myself = discord.Embed(
                description=f'{ctx.author.mention} {random.choice(self_kill_messages)}',
                color=discord.Color.purple()
            )
            await ctx.send(embed=kill_myself)
        else:
            kill_other = discord.Embed(
                description=f'{ctx.author.mention} {random.choice(kill_messages)} {target.mention}.',
                color=discord.Color.purple()
            )
            await ctx.send(embed=kill_other)

    @commands.command()
    async def mean(self, ctx, meanee: discord.Member):

        if meanee == ctx.author:
            mean_world = discord.Embed(
                description=f'{ctx.author.mention} says the world is an cruel place',
                color=discord.Color.purple()
            )
            await ctx.send(embed=mean_world)
        else:
            mean_synonyms = ['cruel', 'mean', 'evil', 'annoying']

            mean_other = discord.Embed(
                description=f'{ctx.author.mention} says {meanee.mention} is {random.choice(mean_synonyms)}.',
                color=discord.Color.purple()
            )
            await ctx.send(embed=mean_other)

    @commands.command()
    async def say(self, ctx, *, speechbubble):
        if speechbubble.endswith('-hide'):

            hiddenspeechbubble = speechbubble[:-5]

            await ctx.channel.purge(limit=1)

            hidden_message = discord.Embed(
                description=hiddenspeechbubble,
                color=discord.Color.purple()
            )
            await ctx.send(embed=hidden_message)
        else:
            unhidden_message = discord.Embed(
                description=speechbubble,
                color=discord.Color.purple()
            )
            await ctx.send(embed=unhidden_message)

    @commands.command()
    async def rob(self, ctx, thievee: discord.Member):
        rob_messages = ['takes life savings of', 'takes coin purse of', 'beats up and robs']

        if thievee == ctx.author:
            rob_self = discord.Embed(
                description=f'{ctx.author.mention} tries to rob themself to no avail.',
                color=discord.Color.purple()
            )
            await ctx.send(rob_self)
        else:
            rob_other = discord.Embed(
                description=f'{ctx.author.mention} {random.choice(rob_messages)} {thievee.mention}.',
                color=discord.Color.purple()
            )
            await ctx.send(embed=rob_other)

    @commands.command()
    async def cookie(self, ctx, cookiee: discord.Member):
        if cookiee == ctx.author:
            gift_self = discord.Embed(
                description=f'{ctx.author.mention} rewards themself with a cookie.',
                color=discord.Color.purple()
            )
            await ctx.send(embed=gift_self)
        else:
            gift_other = discord.Embed(
                description=f'{ctx.author.mention} gifts {cookiee.mention} a cookie.',
                color=discord.Color.purple()
            )
            await ctx.send(embed=gift_other)

    @commands.command()
    async def simp(self, ctx, simpee: discord.Member):
        if simpee == ctx.author:
            simp_message1 = discord.Embed(
                description=f'{ctx.author.mention} simps themself. Slightly narcissistic ngl.',
                color=discord.Color.purple()
            )
            await ctx.send(embed=simp_message1)
        else:

            simp_message2 = discord.Embed(
                description=f'{ctx.author.mention} is a *simp* for {simpee.mention}',
                color=discord.Color.purple()
            )
            await ctx.send(embed=simp_message2)

    @commands.command()
    async def superior(self, ctx, superioree: discord.Member):
        is_sup = ['is literally superior to', 'falsely believes they\'re superior to']

        sup_message = discord.Embed(
            description=f'{ctx.author.mention} {random.choice(is_sup)} {superioree.mention}',
            color=discord.Color.purple()
        )
        await ctx.send(embed=sup_message)


def setup(client):
    client.add_cog(FunCommands(client))
