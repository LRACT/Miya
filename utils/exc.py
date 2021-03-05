import discord
from discord.ext import commands

class Blacklisted(commands.CheckFailure):
    pass

class Forbidden(commands.CheckFailure):
    pass

class No_management(commands.CheckFailure):
    pass
