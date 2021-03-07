import asyncio
import locale

import discord
from discord.ext import commands

from utils import data
from utils import webhook

locale.setlocale(locale.LC_ALL, "")


class DataManagement(commands.Cog, name="데이터 관리"):
    def __init__(self, miya):
        self.miya = miya

    @commands.command(name="가입", aliases=["등록"])
    async def _register(self, ctx):
        rows = await data.fetch(
            f"SELECT * FROM `users` WHERE `user` = '{ctx.author.id}'")
        if not rows:
            embed = discord.Embed(
                title="미야 이용 약관에 동의하시겠어요?",
                description=
                "`미야`의 서비스를 사용하시려면 이용약관에 동의해야 해요.\n`동의합니다`를 입력하여 이용 약관에 동의하실 수 있어요!\n \n[이용 약관](http://miya.kro.kr/tos)\n[개인정보보호방침](http://miya.kro.kr/privacy)",
                color=0x5FE9FF,
            )
            embed.set_author(name="서비스 등록", icon_url=self.miya.user.avatar_url)
            register_msg = await ctx.reply(embed=embed)
            async with ctx.channel.typing():

                def check(msg):
                    return (msg.channel == ctx.channel
                            and msg.author == ctx.author
                            and msg.content == "동의합니다")

                try:
                    msg = await self.miya.wait_for("message",
                                                   timeout=180,
                                                   check=check)
                except asyncio.TimeoutError:
                    fail_embed = discord.Embed(
                        description="미야 이용약관 동의에 시간이 너무 오래 걸려 취소되었습니다.",
                        color=0xFF0000)
                    await register_msg.edit(embed=fail_embed, delete_after=5)
                else:
                    await msg.delete()
                    await register_msg.delete()
                    result = await data.commit(f"")
                    if result == "SUCCESS":
                        await ctx.reply(
                            f"<:cs_yes:659355468715786262> 서버 등록이 완료되었어요! 이제 미야의 기능을 사용하실 수 있어요."
                        )
                    else:
                        await ctx.reply(
                            f"<:cs_no:659355468816187405> 서버 등록 도중에 오류가 발생했어요. 등록을 다시 시도해주세요.\n계속해서 이런 현상이 발생한다면 https://discord.gg/tu4NKbEEnn 로 문의해주세요."
                        )
        else:
            await ctx.reply(
                f"<:cs_id:659355469034422282> 이미 등록되어 있는 유저에요.\n등록되지 않았는데 이 문구가 뜬다면 https://discord.gg/tu4NKbEEnn 로 문의해주세요."
            )


def setup(miya):
    miya.add_cog(DataManagement(miya))
