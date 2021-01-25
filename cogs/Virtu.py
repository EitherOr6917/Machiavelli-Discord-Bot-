# Import statements
from other.CommonBotFunctions import *
from discord.ext import commands
import random
import asyncio


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
        if not is_banned(ctx) and not channel_banned(ctx):
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

    @commands.command(hidden=True, help='Gives specified amount of virtù')
    async def give(self, ctx, amount: int, member: discord.Member = ''):
        if not is_banned(ctx) and not channel_banned(ctx) and is_superuser_or_admin(ctx.author):
            target = ctx.author if member == '' else member
            user = User(target)
            user.add(amount)
            user.try_level_up()
            user.save()
            await ctx.send('Done!')

    @commands.command(hidden=True, help='Gives specified amount of virtù', aliases=['amounttolevel'])
    async def amount_to_level(self, ctx, member: discord.Member = ''):
        if not is_banned(ctx) and not channel_banned(ctx):
            target = ctx.author if member == '' else member
            user = User(target)
            if user.amount_to_level > -1:
                await ctx.send(f'{target.display_name} needs {user.amount_to_level} xp to level up!')
            else:
                await ctx.send(f'{target.display_name} cannot level up any further.')

    @commands.command(help='Become a gambler! Use the slot machine', aliases=['slotmachine', 'slots'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.guild_only()
    async def slot_machine(self, ctx, bet: int):
        if not is_banned(ctx) and not channel_banned(ctx):
            user = User(ctx.author)
            bet = bet
            if user.xp < bet:
                await ctx.send(f'{ctx.author.display_name}, you do not have enough xp to do this.')
                return

            emojis = [':sunny:', ':partly_sunny:', ':cloud:', ':cloud_rain:', ':cloud_lightning:', ':snowflake:']
            results = [random.choice(emojis), random.choice(emojis), random.choice(emojis)]
            total = 1
            text = 'You lost your bet, try again!'

            if results[0] == results[1] or results[1] == results[2] or results[2] == results[0]:
                total = 2
            if results[0] == results[1] == results[2]:
                total = 3

            if total == 1:
                user.remove(bet)
            elif total == 2:
                text = 'You won twice your bet, you can do better!'
                user.add(bet * 2)
            elif total == 3:
                text = 'You won five times your bet, keep your luck going!'
                user.add(bet * 5)

            embed0 = discord.Embed(
                title='- SLOTS -',
                description=f'{results[0]}',
                color=discord.Color.purple()
            )
            message = await ctx.send(embed=embed0)
            embed1 = discord.Embed(
                title='- SLOTS -',
                description=f'{results[0]} {results[1]}',
                color=discord.Color.purple()
            )
            await asyncio.sleep(0.075)
            await message.edit(embed=embed1)
            embed2 = discord.Embed(
                title='- SLOTS -',
                description=f'{results[0]} {results[1]} {results[2]}',
                color=discord.Color.purple()
            )
            await asyncio.sleep(0.075)
            await message.edit(embed=embed2)
            embed3 = discord.Embed(
                title='- SLOTS -',
                description=f'{results[0]} {results[1]} {results[2]}',
                color=discord.Color.purple()
            )
            embed3.set_footer(text=text)
            await asyncio.sleep(0.075)
            await message.edit(embed=embed3)
            user.save()

    @commands.command(help='10 chances to guess the number for extra virtù!', aliases=['guessthenumber'])
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def guess_the_number(self, ctx):
        if not is_banned(ctx) and not channel_banned(ctx):
            user = User(ctx.author)
            guesses = 10
            correct_num = random.randint(1, 100)
            await ctx.send(f'{ctx.author.display_name}, I\'ve selected a number between 1 and 100, take a guess!')

            while guesses > 1:
                try:
                    msg = await self.client.wait_for(
                        'message',
                        check=lambda message: message.author == ctx.author, timeout=90
                    )
                except asyncio.TimeoutError:
                    await ctx.send(f'Sorry {ctx.author.display_name}, your command has timed out.')
                else:
                    try:
                        current_try = int(msg.content)
                    except ValueError:
                        await ctx.send(f'{ctx.author.display_name} please send an integer between 1 and 100.')
                    else:
                        if current_try == correct_num:
                            await ctx.send(f'Congrats {ctx.author.display_name}, you guessed the right number after '
                                           f'{10 - guesses}! For this you win {10 * guesses} virtù.')
                            user.add(10 * guesses)
                            user.save()
                            break
                        elif current_try > correct_num + 25:
                            await ctx.send(f'{ctx.author.display_name}, your guess is way too high!')
                        elif current_try > correct_num:
                            await ctx.send(f'Sorry {ctx.author.display_name}, your guess is too high.')
                        elif current_try < correct_num - 25:
                            await ctx.send(f'Woah there {ctx.author.display_name}, your guess is way too low!')
                        elif current_try < correct_num:
                            await ctx.send(f'Sorry {ctx.author.display_name}, your guess is a bit too low.')
                        guesses -= 1
            if guesses == 1:
                try:
                    msg = await self.client.wait_for(
                        'message',
                        check=lambda message: message.author == ctx.author, timeout=90
                    )
                except asyncio.TimeoutError:
                    await ctx.send(f'Sorry {ctx.author.display_name}, your command has timed out.')
                else:
                    try:
                        current_try = int(msg.content)
                    except ValueError:
                        await ctx.send(f'{ctx.author.display_name} please send an integer between 1 and 100.')
                    else:
                        if current_try == correct_num:
                            await ctx.send(f'Congrats {ctx.author.display_name}, you guessed the right number after '
                                           f'{10 - guesses}! For this you win {10 * guesses} virtù.')
                            user.add(10 * guesses)
                            user.save()
                        else:
                            await ctx.send(f'That was your last chance, better luck next time, '
                                           f'{ctx.author.display_name}!')


def setup(client):
    client.add_cog(Virtu(client))
