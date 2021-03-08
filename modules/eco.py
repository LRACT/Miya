import datetime
import typing

import discord
from discord.ext import commands

from utils import data


class Economy(commands.Cog, name="경제"):
    def __init__(self, miya):
        self.miya = miya

    @commands.command(name="지갑")
    async def _wallet(self, ctx, user: typing.Optional[discord.User] = None):
        if user is None:
            user = ctx.author
        rows = await data.fetch(f"SELECT * FROM `users` WHERE `user` = '{user.id}'")
        if not rows:
            await ctx.reply(f"<:cs_no:659355468816187405> {user}님의 지갑 데이터가 등록되지 않았어요.")
        else:
            embed = discord.Embed(
                title=f"💳 {user}님의 지갑 정보",
                timestamp=datetime.datetime.utcnow(),
                color=0x5FE9FF,
            )
            embed.add_field(name="잔여 코인", value=f"{rows[0][1]}개", inline=False)
            embed.add_field(
                name="곧 더 많은 기능이 찾아옵니다...", value="새로운 기능도 많이 기대해주세요!", inline=False
            )
            embed.set_thumbnail(url=user.avatar_url_as(static_format="png", size=2048))
            embed.set_author(name="지갑", icon_url=self.miya.user.avatar_url)
            await ctx.reply(embed=embed)


def setup(miya):
    miya.add_cog(Economy(miya))
