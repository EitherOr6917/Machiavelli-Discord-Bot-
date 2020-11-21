# Import statements
import discord
from discord.ext import commands


class Cute(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command(help='Says that a member likes another member')
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def likes(self, ctx, target1: discord.Member, target2: discord.Member):
        sitting_message = discord.Embed(
            description=f'{target1.mention} and {target2.mention} sitting in the tree\nK-i-s-s-i-n-g! \nFirst comes '
                        f'love.\nThen comes marriage.\nThen comes baby in the baby carriage.',
            color=discord.Color.purple()
        )

        await ctx.send(embed=sitting_message)


def setup(client):
    client.add_cog(Cute(client))
