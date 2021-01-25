# Import statements
import random
from other.CommonBotFunctions import *


class FunCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command(help='You kill either another person or yourself')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def kill(self, ctx, target: discord.Member):
        if not is_banned(ctx) and not channel_banned(ctx):
            self_kill_messages = ['decided to off themselves.', 'decided the donuts weren\'t good enough.',
                                  'wants to try making toast in a bath',
                                  'decides to become a ceiling fixture.']
            kill_messages = ['shoots', 'plants bomb and explodes', 'runs over', 'contracts Jon Doe to kill']

            if target == ctx.author:
                await ctx.send(f'{ctx.author.display_name} {random.choice(self_kill_messages)}')
            else:
                await ctx.send(f'{ctx.author.display_name} {random.choice(kill_messages)} {target.display_name}.')

    @commands.command(help='Says what you want it to, add "-hide" to hide your message')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def say(self, ctx, *, speechbubble):
        if not is_banned(ctx) and not channel_banned(ctx):
            if speechbubble.endswith('-hide'):

                hiddenspeechbubble = speechbubble[:-5]

                await ctx.message.delete()

                await ctx.send(hiddenspeechbubble)
            else:
                await ctx.send(speechbubble)

    @commands.command(help='Gives another user or yourself a cookie')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def cookie(self, ctx, cookiee: discord.Member):
        if not is_banned(ctx) and not channel_banned(ctx):
            if cookiee == ctx.author:
                await ctx.send(f'{ctx.author.display_name} rewards themself with a cookie.')
            else:
                await ctx.send(f'{ctx.author.display_name} gifts {cookiee.display_name} a cookie.')

    @commands.command(help='You simp the specified user (can be yourself)')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def simp(self, ctx, simpee: discord.Member):
        if not is_banned(ctx) and not channel_banned(ctx):
            if simpee == ctx.author:
                await ctx.send(f'{ctx.author.display_name} simps themself. Slightly narcissistic ngl.')
            else:

                await ctx.send(f'{ctx.author.display_name} is a *simp* for {simpee.display_name}')

    @commands.command(help='Decides whether you or the specifed user are superior')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def superior(self, ctx, superioree: discord.Member):
        if not is_banned(ctx) and not channel_banned(ctx):
            is_sup = ['is literally superior to', 'falsely believes they\'re superior to']

            await ctx.send(f'{ctx.author.display_name} {random.choice(is_sup)} {superioree.display_name}')

    @commands.command(help='Quotes Niccolo Machiavelli')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def quote(self, ctx):
        if not is_banned(ctx) and not channel_banned(ctx):
            machiavelli_quotes = [
                '“Everyone sees what you appear to be, few experience what you really are.”\n― Niccolò Machiavelli, '
                'The Prince',
                '“If an injury has to be done to a man it should be so severe that his vengeance need not be '
                'feared.”\n― '
                'Niccolo Machiavelli, The Prince',
                '“The lion cannot protect himself from traps, and the fox cannot defend himself from wolves. One must '
                'therefore be a fox to recognize traps, and a lion to frighten wolves.”\n― Niccolò Machiavelli, '
                'The Prince',
                '“The first method for estimating the intelligence of a ruler is to look at the men he has around '
                'him.”\n― Niccolò Machiavelli, The Prince',
                '“There is no other way to guard yourself against flattery than by making men understand that telling '
                'you '
                'the truth will not offend you.”\n― Machiavelli Niccolo, The Prince',
                '“Never was anything great achieved without danger.”\n― Niccolo Machiavelli',
                '“Never attempt to win by force what can be won by deception.”\n― Niccolò Machiavelli, The Prince',
                '“it is much safer to be feared than loved because ...love is preserved by the link of obligation '
                'which, '
                'owing to the baseness of men, is broken at every opportunity for their advantage; but fear preserves '
                'you '
                'by a dread of punishment which never fails.”\n― Niccolo Machiavelli, The Prince',
                '“I\'m not interested in preserving the status quo; I want to overthrow it.”\n― Machiavelli Niccolo',
                '“Men are driven by two principal impulses, either by love or by fear.”\n― Niccolò Machiavelli, '
                'The Discourses',
                '“All courses of action are risky, so prudence is not in avoiding danger (it\'s impossible), '
                'but calculating risk and acting decisively. Make mistakes of ambition and not mistakes of sloth. '
                'Develop '
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
                'nor more dangerous to manage than a new system. For the initiator has the enmity of all who would '
                'profit '
                'by the preservation of the old institution and merely lukewarm defenders in those who gain by the new '
                'ones. ”\n― Niccolò Machiavelli '
            ]

            machi_quote = discord.Embed(
                description=random.choice(machiavelli_quotes),
                color=discord.Color.purple()
            )
            await ctx.send(embed=machi_quote)

    @commands.command(aliases=['noballs'], help='Says that the specified user has no balls')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def no_balls(self, ctx, target: discord.Member):
        if not is_banned(ctx) and not channel_banned(ctx):
            await ctx.send(f'{target.display_name} has no balls.')

    @commands.command(aliases=['hasballs'], help='Says that the specified user has balls')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def has_balls(self, ctx, target: discord.Member = 'none'):
        if not is_banned(ctx) and not channel_banned(ctx):
            if target == 'none':
                await ctx.send(f'{ctx.author.display_name} has balls.')
            else:
                await ctx.send(f'{target.display_name} has balls.')

    @commands.command(aliases=['issimp'], help='Specified user is a simp')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def is_simp(self, ctx, target: discord.Member):
        if not is_banned(ctx) and not channel_banned(ctx):
            await ctx.send(f'{target.display_name} is a simp.')

    @commands.command(help='Press F to pay respects (target optional)')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def f(self, ctx, *, target=''):
        if not is_banned(ctx) and not channel_banned(ctx):
            if target == '':
                f_message = f'Press f to pay respects'
            else:
                f_message = f'Press f to pay respects to {target}'

            message = await ctx.send(embed=f_message)
            await message.add_reaction('🇫')

    @commands.command(help='Decides which of the given options wins')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def choose(self, ctx, *, options):
        if not is_banned(ctx) and not channel_banned(ctx):
            option_list = options.split()
            pick = random.choice(option_list)
            await ctx.send(f'{pick} wins.')

    @commands.command(help='Says bruh')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def bruh(self, ctx):
        if not is_banned(ctx) and not channel_banned(ctx):
            await ctx.send(f'bruh')

    @commands.command(aliases=['secretsanta', 'ss'], help='Sends out dms with secret santa targets')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def secret_santa(self, ctx, *people: discord.Member):
        if not is_banned(ctx) and not channel_banned(ctx):
            people_list = list(people)
            random.shuffle(people_list)
            number = len(people_list)
            for i in range(len(people_list)):
                targeter = people_list[i]
                if i == number-1:
                    target = people_list[0]
                else:
                    target = people_list[i + 1]
                await targeter.send(f'Targeter: {targeter} \nTarget: {target}')

    @commands.command(aliases=['goodjob!', 'goodjob'], help='Tell the bot \'good job\'')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def good_job(self, ctx):
        if not is_banned(ctx) and not channel_banned(ctx):
            await ctx.send(f'Awww, thank you {ctx.author.display_name}')

    @commands.command(aliases=['badjob!', 'badjob'], help='Tell the bot \'bad job\'')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def bad_job(self, ctx):
        if not is_banned(ctx) and not channel_banned(ctx):
            random.seed()
            neg_msg = ['Well fuck you', 'I\'m trying my best', 'Fuck offff', 'That\'s rather mean of you']
            await ctx.send(f'{random.choice(neg_msg)} {ctx.author.display_name}')

    @commands.command(help='Does nothing')
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.guild_only()
    async def nothing(self, ctx):
        return

    @commands.command(aliases=['dumbfucker'], help='The specified user is dumb asf')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def dumb_fucker(self, ctx, bad_person: discord.Member):
        if not is_banned(ctx) and not channel_banned(ctx):
            await ctx.send(f'{bad_person.display_name} is one dumb motherfucker.')

    @commands.command(help='Oh my G.')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def omyg(self, ctx):
        if not is_banned(ctx) and not channel_banned(ctx):
            await ctx.message.delete()
            messages = await ctx.channel.history(limit=1).flatten()
            message = messages[0]
            await message.add_reaction('🇬')
            await ctx.send(f'Oh my G')

    @commands.command(help='Cards against humanity', aliases=['cardsagainsthumanity', 'cah'])
    @commands.guild_only()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def cards_against_humanity(self, ctx):
        if not is_banned(ctx) and not channel_banned(ctx):
            with open('jsons/cahcards.json', 'r') as file:
                cards = json.load(file)
                white_cards = cards['white']
                black_cards = cards['black']


def setup(client):
    client.add_cog(FunCommands(client))
