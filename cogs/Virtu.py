# Import statements
import discord
import json
from discord.ext import commands
import random
from other import CommonBotFunctions


# Async definitions
async def change_virtu(ctx, amount):
    with open('jsons/virtuRecord.json', 'r') as file:
        virtu_amount = json.load(file)

    if str(ctx) in virtu_amount:
        if amount < 0:
            virtu_amount[str(ctx)] -= abs(amount)
        elif amount > 0:
            virtu_amount[str(ctx)] += amount
        else:
            print('ERROR: Don\'t chance virtu by 0. That is dumb.')

        with open('jsons/virtuRecord.json', 'w') as file:
            json.dump(virtu_amount, file, indent=4)

    else:
        virtu_amount[str(ctx)] = 1

        with open('jsons/virtuRecord.json', 'w') as file:
            json.dump(virtu_amount, file, indent=4)


async def check_virtu(userid):
    with open('jsons/virtuRecord.json', 'r') as file:
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
            with open('jsons/virtuLevels.json', 'r') as f2:
                virtu_levels = json.load(f2)

            if str(message.author.id) not in virtu_levels:
                virtu_levels[str(message.author.id)] = 1
                with open('jsons/virtuLevels.json', 'w') as f3:
                    json.dump(virtu_levels, f3, indent=4)

            await change_virtu(message.author.id, (virtu_levels[str(message.author.id)]))

    # Commands
    @commands.command(help='Shows user\'s amount of virtù')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def virtu(self, ctx, target: discord.Member = ''):
        if not CommonBotFunctions.is_banned(ctx) and not CommonBotFunctions.channel_banned(ctx):
            citizen = target
            if citizen == '':
                citizen = ctx.author

            with open('jsons/virtuRecord.json', 'r') as file:
                virtu_record_list = json.load(file)

            if str(citizen.id) not in virtu_record_list:
                virtu_record_list[str(citizen.id)] = 0
                with open('jsons/virtuRecord.json', 'w') as file:
                    json.dump(virtu_record_list, file, indent=4)

            with open('jsons/virtuLevels.json', 'r') as file:
                virtu_levels_list = json.load(file)

            if str(citizen.id) not in virtu_levels_list:
                virtu_levels_list[str(citizen.id)] = 1
                with open('jsons/virtuLevels.json', 'w') as file:
                    json.dump(virtu_levels_list, file, indent=4)

            # Changes citizen level is necessary
            current_citizen_level = virtu_levels_list[str(citizen.id)]
            temp_record_editable = virtu_record_list[str(citizen.id)]
            level_up_cost = 250*current_citizen_level
            if temp_record_editable >= level_up_cost:
                leveling_up = int(temp_record_editable/level_up_cost)
                virtu_levels_list[str(citizen.id)] += leveling_up
                virtu_record_list[str(citizen.id)] -= level_up_cost

                with open('jsons/virtuLevels.json', 'w') as file:
                    json.dump(virtu_levels_list, file, indent=4)
                with open('jsons/virtuRecord.json', 'w') as file:
                    json.dump(virtu_record_list, file, indent=4)

            # Sends embeded message
            virtu_msg = discord.Embed(
                title=f'{citizen.display_name}\'s Virtù',
                description=f'Virtù Level: {virtu_levels_list[str(citizen.id)]}\nVirtù total: '
                            f'{virtu_record_list[str(citizen.id)]}',
                color=discord.Color.purple()
            )
            virtu_msg.set_thumbnail(url=citizen.avatar_url)

            await ctx.send(embed=virtu_msg)

    @commands.command(help='Attempts to take virtu from the target')
    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def rob(self, ctx, target: discord.Member, amount: int):
        if CommonBotFunctions.is_banned(ctx) or CommonBotFunctions.channel_banned(ctx):
            return
        random.seed()
        robber_savings = await check_virtu(ctx.author.id)
        target_savings = await check_virtu(target.id)
        chance = int(await check_virtu(target.id)/await check_virtu(ctx.author.id)*50)
        if robber_savings >= amount > 0 and target_savings >= amount:
            result = random.randint(1, (100+chance))
            if result <= 55:
                await change_virtu(ctx.author.id, -1*amount)
                await change_virtu(target.id, amount)
                await ctx.send(f'{ctx.author.mention} screwed up the robbery.')
            else:
                await change_virtu(ctx.author.id, amount)
                await change_virtu(target.id, (-1 * amount))
                await ctx.send(f'{ctx.author.mention} successfully pulled off the robbery.')
        else:
            await ctx.send(f'{ctx.author.mention} you or the target do not have enough virtù to do this')

    @commands.command(help='Give another member some of your virtù')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def give(self, ctx, target: discord.Member, amount: int):
        if not CommonBotFunctions.is_banned(ctx) and not CommonBotFunctions.channel_banned(ctx):
            if await check_virtu(ctx.author.id) >= amount:
                await change_virtu(ctx.author.id, -1 * amount)
                await change_virtu(target.id, amount)

                await ctx.send(f'{ctx.author.mention} you gave {target.mention} {amount} virtù')
            else:
                await ctx.send(f'{ctx.author.mention} you do not have enough virtù to do this.')

    @commands.command(hidden=True, help='Creates Virtù which is given to user')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def sgive(self, ctx, target: discord.Member, amount: int):
        if not CommonBotFunctions.is_banned(ctx) and not CommonBotFunctions.channel_banned(ctx):
            if ctx.author.id == 406663932166668288:
                await change_virtu(target.id, amount)

                await ctx.send(f'{target.mention} now has {amount} more virtù')
            else:
                await ctx.send(f'{ctx.author.mention} you cannot do this.')


def setup(client):
    client.add_cog(Virtu(client))
