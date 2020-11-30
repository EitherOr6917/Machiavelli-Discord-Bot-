# Import statements
import discord
from discord.ext import commands
import json
import random


# Functions
def is_banned(ctx):
    with open('jsons/banned.json', 'r') as file:
        banned_users = json.load(file)

    return str(ctx.author.id) in banned_users


def channel_banned(ctx):
    with open('jsons/bannedChannels.json', 'r') as file:
        banned_channels = json.load(file)

    return str(ctx.channel.id) in banned_channels


class Cute(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands


def setup(client):
    client.add_cog(Cute(client))
