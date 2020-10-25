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
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix=get_prefix, intents=intents)


# Events
@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes[str(guild.id)] = '>'

    with open('prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)


# Commands
@client.command(hidden=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

    load_message = discord.Embed(
        description=f'Loaded {extension}',
        color=discord.Color.purple()
    )
    await ctx.send(embed=load_message)


@client.command(hidden=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

    unload_message = discord.Embed(
        description=f'Unloaded {extension}',
        color=discord.Color.purple()
    )
    await ctx.send(embed=unload_message)


# Running the client
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(token)
