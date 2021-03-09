import datetime
import typing
import random

import discord
from discord.ext import commands

from utils import data


class Economy(commands.Cog, name="경제"):
    def __init__(self, miya):
        self.miya = miya

    def in_guild(ctx):
        return ctx.guild.id == 564418977627897887

    @commands.command(name="지갑")
    @in_guild()
    async def _wallet(self, ctx, user: typing.Optional[discord.User] = None):
        """
        미야야 지갑 [ @유저 ]


        지정한 유저( 혹은 본인 )의 지갑 정보를 확인합니다.
        """
        if user is None:
            user = ctx.author
        rows = await data.fetch(
            f"SELECT * FROM `users` WHERE `user` = '{user.id}'")
        if not rows:
            await ctx.reply(
                f"<:cs_no:659355468816187405> {user}님의 지갑 데이터가 등록되지 않았어요.")
        else:
            embed = discord.Embed(
                title=f"💳 {user}님의 지갑 정보",
                timestamp=datetime.datetime.utcnow(),
                color=0x5FE9FF,
            )
            embed.add_field(name="잔여 코인", value=f"{rows[0][1]}개", inline=False)
            embed.add_field(name="곧 더 많은 기능이 찾아옵니다...",
                            value="새로운 기능도 많이 기대해주세요!",
                            inline=False)
            embed.set_thumbnail(
                url=user.avatar_url_as(static_format="png", size=2048))
            embed.set_author(name="지갑", icon_url=self.miya.user.avatar_url)
            await ctx.reply(embed=embed)

    @commands.command(name="도박")
    @in_guild()
    async def _gamble(self, ctx, money):
        rows = await data.fetch(f"SELECT * FROM `users` WHERE `user` = '{ctx.author.id}'")
        if money in ["모두", "전체", "올인"]:
            money = rows[0][1]
        elif money.isdecimal() is not True:
            raise commands.BadArgument

        user = random.randint(1, 6)
        bot = random.randint(1, 6)
        embed, rest = None, None
        if user < bot:
            embed = discord.Embed(
                title="🎲 {user}님의 주사위 도박 결과", timestamp=datetime.datetime.utcnow(), color=0xFF9999)
            embed.set_footer(text="모두 잃어버린 나")
            rest = int(rows[0][1]) - int(money)
        elif user == bot:
            embed = discord.Embed(
                title="🎲 {user}님의 주사위 도박 결과", timestamp=datetime.datetime.utcnow(), color=0x333333)
            embed.set_footer(text="그래도 잃지는 않은 나")
            rest = int(rows[0][1])
        elif user > bot:
            embed = discord.Embed(
                title="🎲 {user}님의 주사위 도박 결과", timestamp=datetime.datetime.utcnow(), color=0x99FF99)
            embed.set_footer(text="봇을 상대로 모든 것을 가져간 나")
            rest = int(rows[0][1]) + int(money)
        embed.set_author(name="카케구루이", icon_url=self.miya.user.avatar_url)
        embed.set_thumbnail(url=ctx.author.avatar_url_as(
            static_format="png", size=2048))
        embed.add_field(name="미야의 주사위", value=f"`🎲 {bot}`", inline=True)
        embed.add_field(name="당신의 주사위", value=f"`🎲 {user}`", inline=True)
        await data.commit(f"UPDATE `users` SET `money` = '{rest}' WHERE `user` = '{ctx.author.id}'")
        await ctx.reply(embed=embed)


def setup(miya):
    miya.add_cog(Economy(miya))
