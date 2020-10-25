# Created by Isaac Nelson

# Basic embed template:
# <variable_name> = discord.Embed(
#             description=<message>,
#             color=discord.Color.purple()
#         )
#         await ctx.send(embed=<variable_name>)

# Import statements
import discord
import os
from discord.ext import commands
import logging

logging.basicConfig(level=logging.INFO)

# Variable declarations
token = os.environ.get('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='>' or commands.when_mentioned, intents=intents)


# Cog loading and unloading
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
