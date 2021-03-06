import datetime
import locale
import typing

import discord
from discord.ext import commands

import utils

locale.setlocale(locale.LC_ALL, "")


class Administration(commands.Cog, name="관리"):
    def __init__(self, miya):
        self.miya = miya

    def is_manager():
        mgr = commands.check(utils.get.mgr)
        if mgr == False:
            raise commands.NotOwner
        return mgr

    @commands.command(name="제한")
    @is_manager()
    async def _black_word(self, ctx, todo, *, word):
        """
        미야야 제한 < 추가 / 삭제 > < 단어 >


        자동 차단 단어를 관리합니다.
        """
        if todo == "추가":
            result = await utils.data.commit(
                f"INSERT INTO `forbidden`(`word`) VALUES('{word}')")
            if result == "SUCCESS":
                await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
                await utils.webhook.blacklist(
                    f"New Forbidden >\nAdmin - {ctx.author} ({ctx.author.id})\nPhrase - {word}",
                    "제한 기록",
                    self.miya.user.avatar_url,
                )
            else:
                await ctx.message.add_reaction("<:cs_no:659355468816187405>")
        elif todo == "삭제":
            result = await utils.data.commit(
                f"DELETE FROM `forbidden` WHERE `word` = '{word}'")
            if result == "SUCCESS":
                await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
                await utils.webhook.blacklist(
                    f"Removed Forbidden >\nAdmin - {ctx.author} ({ctx.author.id})\nPhrase - {word}",
                    "제한 기록",
                    self.miya.user.avatar_url,
                )
            else:
                await ctx.message.add_reaction("<:cs_no:659355468816187405>")
        else:
            raise commands.BadArgument

    @commands.command(name="블랙")
    @is_manager()
    async def blacklist_management(
            self,
            ctx,
            todo,
            id,
            *,
            reason: typing.Optional[str] = "사유가 지정되지 않았습니다."):
        """
        미야야 블랙 < 추가 / 삭제 > < ID > [ 사유 ]


        ID를 통해 유저나 서버의 블랙리스트를 관리합니다.
        """
        date = datetime.datetime.utcnow()
        time = await utils.get.kor_time(date)
        if todo == "추가":
            result = await utils.data.commit(
                f"INSERT INTO `blacklist`(`id`, `reason`, `admin`, `datetime`) VALUES('{id}', '{reason}', '{ctx.author.id}', '{time}')"
            )
            if result == "SUCCESS":
                await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
                await utils.webhook.blacklist(
                    f"New Block >\nVictim - {id}\nAdmin - {ctx.author} ({ctx.author.id})\nReason - {reason}",
                    "제한 기록",
                    self.miya.user.avatar_url,
                )
            else:
                await ctx.message.add_reaction("<:cs_no:659355468816187405>")
        elif todo == "삭제":
            result = await utils.data.commit(
                f"DELETE FROM `blacklist` WHERE `id` = '{id}'")
            if result == "SUCCESS":
                await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
                await utils.webhook.blacklist(
                    f"Removed Block >\nUnblocked - {id}\nAdmin - {ctx.author} ({ctx.author.id})",
                    "제한 기록",
                    self.miya.user.avatar_url,
                )
            else:
                await ctx.message.add_reaction("<:cs_no:659355468816187405>")
        else:
            raise commands.BadArgument

    @commands.command(name="탈주")
    @commands.is_owner()
    async def _leave(self, ctx, guild_id: int):
        """
        미야야 탈주 < ID >


        지정한 서버에서 미야가 나갑니다.
        """
        guild = self.miya.get_guild(int(guild_id))
        if guild is not None:
            await guild.leave()
            await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
        else:
            await ctx.reply("<:cs_no:659355468816187405> 서버를 발견하지 못했어요.")


def setup(miya):
    miya.add_cog(Administration(miya))
