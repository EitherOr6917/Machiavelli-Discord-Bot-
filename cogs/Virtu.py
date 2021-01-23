# Import statements
from other import CommonBotFunctions
from other.CommonBotFunctions import *
from discord.ext import commands


class Virtu(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        if message.author != self.client.user:
            user = User(message.author)
            user.add(1)
            user.save()

    # Commands
    @commands.command(help='Shows user\'s amount of virtù')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def virtu(self, ctx, member: discord.Member = ''):
        if not CommonBotFunctions.is_banned(ctx) and not CommonBotFunctions.channel_banned(ctx):
            target = ctx.author if member == '' else member
            user = User(target)

            embed = discord.Embed(
                title=f'{target.display_name}\'s Virtù',
                description=f'Virtù Level: {user.level}\nVirtù Xp: {user.xp}',
                color=discord.Color.purple()
            )
            embed.set_thumbnail(url=target.avatar_url)
            embed.set_footer(text=user.id)

            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Virtu(client))
