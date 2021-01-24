import json
import discord
from discord.ext import commands


def is_superuser_or_admin(member: discord.Member):
    user = User(member)
    return user.level == 100 or member.guild_permissions.administrator


def is_owner(ctx: commands.Context):
    return ctx.author.id == 406663932166668288


def is_banned(ctx):
    with open('jsons/banned.json', 'r') as file:
        banned_users = json.load(file)

    return str(ctx.author.id) in banned_users


def channel_banned(ctx):
    with open('jsons/bannedChannels.json', 'r') as file:
        banned_channels = json.load(file)

    return str(ctx.channel.id) in banned_channels


def prefix(ctx):
    with open('jsons/prefixes.json', 'r') as file:
        prefixes = json.load(file)
        return prefixes[str(ctx.guild.id)]


class User:
    def __init__(self, member: discord.Member):
        with open('jsons/virtu.json', 'r') as file:
            data = json.load(file)
        self._id = str(member.id)
        self._level = data[self._id]['level'] if self._id in data else 0
        self._xp = data[self._id]['xp'] if self._id in data else 0
        self._amount_to_level = 5 * (self._level+1) ** 2

    # Functions
    def try_level_up(self):
        while self._xp >= self._amount_to_level and self._level < 99:
            self._xp -= self._amount_to_level
            self._level += 1
            self._amount_to_level = 5 * (self._level+1) ** 2

    def add(self, amount: int):
        self._xp += amount
        self.try_level_up()

    def remove(self, amount: int):
        self._xp -= amount

    def super_user(self):
        self._level = 100

    # Serialization
    def save(self):
        with open('jsons/virtu.json', 'r') as file:
            data = json.load(file)

        if self._id not in data:
            data[self._id] = {}

        data[self._id]['xp'] = self._xp
        data[self._id]['level'] = self._level

        with open('jsons/virtu.json', 'w') as file:
            json.dump(data, file, indent=4)

    # Properties
    @property
    def xp(self):
        return self._xp

    @property
    def level(self):
        return self._level

    @property
    def id(self):
        return self._id

    @property
    def amount_to_level(self):
        return self._amount_to_level
