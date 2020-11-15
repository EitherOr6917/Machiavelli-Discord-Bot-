# Import statements
import discord
import random
from discord.ext import commands


class FunCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command(help='You kill either another person or yourself')
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

    @commands.command(help='Says a member is mean')
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

    @commands.command(help='Says what you want it to, add "-hide" to hide your message')
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

    @commands.command(help='You rob whoever you specify')
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

    @commands.command(help='Gives another user or yourself a cookie')
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

    @commands.command(help='You simp the specified user (can be yourself)')
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

    @commands.command(help='Decides whether you or the specifed user are superior')
    async def superior(self, ctx, superioree: discord.Member):
        is_sup = ['is literally superior to', 'falsely believes they\'re superior to']

        sup_message = discord.Embed(
            description=f'{ctx.author.mention} {random.choice(is_sup)} {superioree.mention}',
            color=discord.Color.purple()
        )
        await ctx.send(embed=sup_message)

    @commands.command(help='Quotes Niccolo Machiavelli')
    async def quote(self, ctx):
        machiavelli_quotes = [
            '“Everyone sees what you appear to be, few experience what you really are.”\n― Niccolò Machiavelli, '
            'The Prince',
            '“If an injury has to be done to a man it should be so severe that his vengeance need not be feared.”\n― '
            'Niccolo Machiavelli, The Prince',
            '“The lion cannot protect himself from traps, and the fox cannot defend himself from wolves. One must '
            'therefore be a fox to recognize traps, and a lion to frighten wolves.”\n― Niccolò Machiavelli, '
            'The Prince',
            '“The first method for estimating the intelligence of a ruler is to look at the men he has around '
            'him.”\n― Niccolò Machiavelli, The Prince',
            '“There is no other way to guard yourself against flattery than by making men understand that telling you '
            'the truth will not offend you.”\n― Machiavelli Niccolo, The Prince',
            '“Never was anything great achieved without danger.”\n― Niccolo Machiavelli',
            '“Never attempt to win by force what can be won by deception.”\n― Niccolò Machiavelli, The Prince',
            '“it is much safer to be feared than loved because ...love is preserved by the link of obligation which, '
            'owing to the baseness of men, is broken at every opportunity for their advantage; but fear preserves you '
            'by a dread of punishment which never fails.”\n― Niccolo Machiavelli, The Prince',
            '“I\'m not interested in preserving the status quo; I want to overthrow it.”\n― Machiavelli Niccolo',
            '“Men are driven by two principal impulses, either by love or by fear.”\n― Niccolò Machiavelli, '
            'The Discourses',
            '“All courses of action are risky, so prudence is not in avoiding danger (it\'s impossible), '
            'but calculating risk and acting decisively. Make mistakes of ambition and not mistakes of sloth. Develop '
            'the strength to do bold things, not the strength to suffer.”\n― Niccolo Machiavelli',
            '“It is not titles that honour men, but men that honour titles.”\n― Niccolò Machiavelli',
            '“…he who seeks to deceive will always find someone who will allow himself to be deceived.”\n― '
            'Machiavelli Niccolo, The Prince',
            '“The vulgar crowd always is taken by appearances, and the world consists chiefly of the vulgar.”\n― '
            'Niccolò Machiavelli, The Prince',
            '“He who wishes to be obeyed must know how to command”\n― Niccolò Machiavelli, The Prince',
            '“There is nothing more important than appearing to be religious.”\n― Niccolò Machiavelli',
            '“Whosoever desires constant success must change his conduct with the times.”\n― Niccolo Machiavelli',
            '“Of mankind we may say in general they are fickle, hypocritical, and greedy of gain.”\n― Niccolò '
            'Machiavelli, The Prince',
            '“It must be remembered that there is nothing more difficult to plan, more doubtful of success, '
            'nor more dangerous to manage than a new system. For the initiator has the enmity of all who would profit '
            'by the preservation of the old institution and merely lukewarm defenders in those who gain by the new '
            'ones. ”\n― Niccolò Machiavelli '
        ]

        machi_quote = discord.Embed(
            description=random.choice(machiavelli_quotes),
            color=discord.Color.purple()
        )
        await ctx.send(embed=machi_quote)

    @commands.command(help='Says that the specified user has no balls')
    async def noballs(self, ctx, target: discord.Member):
        noball_message = discord.Embed(
            description=f'{target.mention} has no balls.',
            color=discord.Color.purple()
        )

        await ctx.send(embed=noball_message)

    @commands.command(help='Says that the specified user has balls')
    async def hasballs(self, ctx, target: discord.Member = 'none'):
        if target == 'none':
            ball_message = discord.Embed(
                description=f'{ctx.author.mention} has balls.',
                color=discord.Color.purple()
            )
        else:
            ball_message = discord.Embed(
                description=f'{target.mention} has balls.',
                color=discord.Color.purple()
            )

        await ctx.send(embed=ball_message)

    @commands.command(help='Specified user is a simp')
    async def simp(self, ctx, target: discord.Member):
        simp_message = discord.Embed(
            description=f'{target.mention} is a simp.',
            color=discord.Color.purple()
        )

        await ctx.send(embed=simp_message)

    @commands.command(help='Press F to pay respects (target optional)')
    async def f(self, ctx, *, target=''):
        if target == '':
            f_message = discord.Embed(
                description=f'Press f to pay respects',
                color=discord.Color.purple()
            )
        else:
            f_message = discord.Embed(
                description=f'Press f to pay respects to {target}',
                color=discord.Color.purple()
            )

        message = await ctx.send(embed=f_message)

        await message.add_reaction('🇫')


def setup(client):
    client.add_cog(FunCommands(client))
