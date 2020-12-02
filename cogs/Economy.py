# Import statements
import discord
from discord.ext import commands
import json


# Functions
def is_banned(ctx):
    with open('jsons/banned.json', 'r') as file:
        banned_users = json.load(file)

    return str(ctx.author.id) in banned_users


def channel_banned(ctx):
    with open('jsons/bannedChannels.json', 'r') as file:
        banned_channels = json.load(file)

    return str(ctx.channel.id) in banned_channels


def getEconRecord():
    with open('jsons/economyRecord.json', 'r') as file:
        econList = json.load(file)
        return econList


def dumpEconRecord(econ_list):
    with open('jsons/economyRecord.json', 'w') as file:
        json.dump(econ_list, file, indent=4)


class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands
    @commands.command(aliases=['ustats'], help='Check your stats')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def user_stats(self, ctx, target: discord.Member = None):
        if not is_banned(ctx) and not channel_banned(ctx):
            econ_record_dict = getEconRecord()
            user = ctx.author if target is None else target
            userid = user.id

            if userid not in econ_record_dict['people']:
                econ_record_dict['people'][userid] = {'balance': 100, 'majority_shareholder_in': [], 'stock_owned': {}}
                dumpEconRecord(econ_record_dict)

            balance = econ_record_dict['people'][userid]['balance']
            maj_share = econ_record_dict['people'][userid]['majority_shareholder_in']
            stocks = econ_record_dict['people'][userid]['stock_owned']
            mj_listing = '*No companies.*' if maj_share == [] else maj_share
            stock_listing = '*No companies*.' if stocks == {} else stocks

            stat_list = discord.Embed(
                description=f'Balance: ${balance}\nMajority shareholder in: {mj_listing}\nHolds stock in: '
                            f'{stock_listing}',
                color=discord.Color.purple()
            )
            stat_list.set_author(name=f'{user.display_name}\'s Account Details', icon_url=user.avatar_url)
            await ctx.send(embed=stat_list)

    @commands.command(aliases=['cstats'], help='Check company\'s stats')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def company_stats(self, ctx, *, name: str):
        if not is_banned(ctx) and not channel_banned(ctx):
            econ_record_dict = getEconRecord()
            company_name = name

            if company_name not in econ_record_dict['companies']:
                await ctx.send(f'{ctx.author.mention}, this company doesn\'t exist!')

            private_s = econ_record_dict['companies'][company_name]['isPrivate']
            share_count = econ_record_dict['companies'][company_name]['shares']
            private_public = 'Private' if private_s is True else 'Public'
            level = econ_record_dict['companies'][company_name]['level']

            stat_list = discord.Embed(
                description=f'Status: {private_public}\n Level: {level}\nTotal share count: {share_count}',
                color=discord.Color.purple()
            )
            stat_list.set_author(name=f'{company_name} Information')
            await ctx.send(embed=stat_list)

    @commands.command(help='Start a business')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def start_company(self, ctx, *, name: str):
        if not is_banned(ctx) and not channel_banned(ctx):
            econ_record_dict = getEconRecord()
            user = ctx.author
            userid = user.id

            if name not in econ_record_dict['companies']:
                econ_record_dict['companies'][name] = {'level': 1, 'isPrivate': True, 'shares': 100, 'avatarURL': "",
                                                       'shareholders': {userid: 100}}
            dumpEconRecord(econ_record_dict)

            await ctx.send(f'{user.mention}, your company has been created. Use the company_stats command to view it.')


def setup(client):
    client.add_cog(Economy(client))
