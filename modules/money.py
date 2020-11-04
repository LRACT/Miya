import discord
from discord.ext import commands
from utils import data
import typing
import locale
locale.setlocale(locale.LC_ALL, '')

class Economy(commands.Cog, name="경제/돈"):
    def __init__(self, miya):
        self.miya = miya
    
    @commands.command(name="돈")
    async def balance(self, ctx, user: typing.Optional[discord.User] = None):
        if user is None:
            user = ctx.author
        result = await data.load('users', 'user', user.id)
        if result is not None:
            embed = discord.Embed(title=f"{user}님의 자산 정보", description="", color=)
            await ctx.send(ctx.author.mention, embed=embed)

def setup(miya):
    miya.add_cog(Economy(miya))