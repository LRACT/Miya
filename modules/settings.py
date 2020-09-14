import discord
from discord.ext import commands

class settings(commands.Cog):
    def __init__(self, miya):
        self.miya = miya
    
    @commands.command(name="설정")
    async def _settings(self, ctx, *args):
        if args[0]

def setup(miya):
    miya.add_cog(settings(miya))