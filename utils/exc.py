import discord
from discord.ext import commands

class Forbidden(commands.CheckFailure):
    def __init__(self, embed, ctx):
        self.embed = embed
        super().__init__(f'<a:ban_guy:761149578216603668> {ctx.author.mention} https://discord.gg/tu4NKbEEnn')

class No_management(commands.CheckFailure):
    pass
