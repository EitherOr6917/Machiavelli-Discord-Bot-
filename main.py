# Created by Isaac Nelson

# Import statements
import discord
import os
from discord.ext import commands
import logging
import json

# Variable declarations
token = os.environ.get('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True
logging.basicConfig(level=logging.INFO)


# Prefixes
def get_prefix(client, message):
    with open('jsons/prefixes.json', 'r') as file:
        prefixes = json.load(file)

    return prefixes[str(message.guild.id)]


def is_banned(ctx):
    with open('jsons/banned.json', 'r') as file:
        banned_users = json.load(file)

    return str(ctx.author.id) in banned_users


def channel_banned(ctx):
    with open('jsons/bannedChannels.json', 'r') as file:
        banned_channels = json.load(file)

    return str(ctx.channel.id) in banned_channels


client = commands.Bot(command_prefix=get_prefix, intents=intents)


# Events
@client.event
async def on_guild_join(guild):
    with open('jsons/prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes[str(guild.id)] = '>'

    with open('jsons/prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)


@client.event
async def on_guild_remove(guild):
    with open('jsons/prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes.pop(str(guild.id))

    with open('jsons/prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)


# Commands
@client.command(hidden=True)
async def load(ctx, extension):
    if ctx.author.id == 406663932166668288:
        client.load_extension(f'cogs.{extension}')

        load_message = discord.Embed(
            description=f'Loaded {extension}',
            color=discord.Color.purple()
        )
        await ctx.send(embed=load_message)


@client.command(hidden=True)
async def unload(ctx, extension):
    if ctx.author.id == 406663932166668288:
        client.unload_extension(f'cogs.{extension}')

        unload_message = discord.Embed(
            description=f'Unloaded {extension}',
            color=discord.Color.purple()
        )
        await ctx.send(embed=unload_message)


@client.command(hidden='true', help='Makes bot unusable')
async def deactivate(ctx):
    if not is_banned(ctx) and not channel_banned(ctx):
        if ctx.author.id == 406663932166668288:
            goodbye_msg = discord.Embed(
                description=f'Goodbye for now.',
                color=discord.Color.dark_gray()
            )

            for fn in os.listdir('./cogs'):
                if fn.endswith('.py'):
                    client.unload_extension(f'cogs.{fn[:-3]}')

            await ctx.send(embed=goodbye_msg)
        else:
            await ctx.send(f'{ctx.author.mention} you may not use this command.')


@client.command(hidden='true', help='Makes bot usable')
async def activate(ctx):
    if not is_banned(ctx) and not channel_banned(ctx):
        if ctx.author.id == 406663932166668288:
            imback_msg = discord.Embed(
                description=f'I\'m back!',
                color=discord.Color.dark_gray()
            )

            for fn in os.listdir('./cogs'):
                if fn.endswith('.py'):
                    client.load_extension(f'cogs.{fn[:-3]}')

            await ctx.send(embed=imback_msg)
        else:
            await ctx.send(f'{ctx.author.mention} you may not use this command.')


# Running the client
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(token)
