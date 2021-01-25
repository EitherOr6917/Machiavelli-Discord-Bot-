# Import statements
import discord
from discord.ext import commands
import random
from other import CommonBotFunctions


class Sus(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command(help='Says that a member likes another member')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def likes(self, ctx, target1: discord.Member, target2: discord.Member):
        if not CommonBotFunctions.is_banned(ctx) and not CommonBotFunctions.channel_banned(ctx):
            await ctx.send(f'{target1.display_name} and {target2.display_name} sitting in the tree\nK-i-s-s-i-n-g! '
                           f'\nFirst comes love.\nThen comes marriage.\nThen comes a baby in the baby carriage.')

    @commands.command(help='Smash someone', hidden=True)
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def smash(self, ctx, target: discord.Member):
        if not CommonBotFunctions.is_banned(ctx) and not CommonBotFunctions.channel_banned(ctx):
            await ctx.send(f'{ctx.author.display_name} wants to smash {target.display_name}')

    @commands.command(help='Specifies who is sus')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def sus(self, ctx, target: discord.Member):
        if not CommonBotFunctions.is_banned(ctx) and not CommonBotFunctions.channel_banned(ctx):
            await ctx.send(f'{ctx.author.display_name} thinks {target.display_name} is sus 😏')

    @commands.command(help='Says who is in the cult', hidden=True)
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def cummiecult(self, ctx, target: discord.Member):
        if not CommonBotFunctions.is_banned(ctx) and not CommonBotFunctions.channel_banned(ctx):
            result = random.randint(1, 10)
            if result != 1:
                msg = discord.Embed(
                    description=f'{target.display_name} is part of the cummie cult',
                    color=discord.Color.purple()
                )
                await ctx.send(embed=msg)
            else:
                msg = discord.Embed(
                    description=f'{ctx.author.display_name} is part of the cummie cult',
                    color=discord.Color.purple()
                )
                await ctx.send(embed=msg)

    @commands.command(help='Choke the shit out of', hidden=True, aliases=['choek'])
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def choektheshitouta(self, ctx, target: discord.Member):
        if not CommonBotFunctions.is_banned(ctx) and not CommonBotFunctions.channel_banned(ctx):
            msg = discord.Embed(
                description=f'{ctx.author.display_name} chokes the shit out of {target.display_name}',
                color=discord.Color.purple()
            )
            msg.set_image(url='https://media.tenor.com/images/22563b2b0db01c6f54df5721a7328e26/tenor.png')
            await ctx.send(embed=msg)

    @commands.command(aliases=['fuckyou'], hidden=True)
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def fuck_you(self, ctx, target: discord.Member):
        await ctx.send(f'{ctx.author.display_name} wants to fuck {target.display_name}')

    @commands.command(help='The specified user is bad', hidden=True)
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def is_bad(self, ctx, bad_person: discord.Member):
        if ctx.author.id != 406663932166668288:  # Checking if I was the one to initiate the command
            await ctx.send(f'{ctx.author.display_name} wants to do bad things to  {bad_person.display_name}')
        else:
            await ctx.send(f'{bad_person.display_name} is bad.')


def setup(client):
    client.add_cog(Sus(client))
