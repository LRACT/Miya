import discord
from discord.ext import commands
import typing
import utils
import locale
locale.setlocale(locale.LC_ALL, '')

def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

class Development(commands.Cog, name="개발"):
    def __init__(self, miya):
        self.miya = miya

    @commands.command(name="제한")
    @commands.is_owner()
    async def _black_word(self, ctx, todo, *, word):
        """
        미야야 제한 < 추가 / 삭제 > < 단어 >
        
        
        특정 단어 사용 시 미야 사용이 제한되게 합니다.
        """
        if todo == "추가":
            result = await utils.data.commit(f"INSERT INTO `forbidden`(`word`) VALUES('{word}')")
            if result == "SUCCESS":
                await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
        elif todo == "삭제":
            result = await utils.data.commit(f"DELETE FROM `forbidden` WHERE `word` = '{word}'")
            if result == "SUCCESS":
                await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
        else:
            await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 제한 < 추가 / 삭제 > < 단어 >`(이)가 올바른 명령어에요!")


    @commands.command(name="블랙")
    @commands.is_owner()
    async def blacklist_management(self, ctx, todo, id, *, reason: typing.Optional[str] = "사유가 지정되지 않았습니다."):
        """
        미야야 블랙 < 추가 / 삭제 > < ID > [ 사유 ]

        
        ID를 통해 유저나 서버의 블랙리스트를 관리합니다.
        """
        time = await utils.get.kor_time()
        if todo == "추가":
            result = await utils.data.commit(f"INSERT INTO `blacklist`(`id`, `reason`, `admin`, `datetime`) VALUES('{id}', '{reason}', '{ctx.author.id}', '{time}')")
            if result == "SUCCESS":
                await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
        elif todo == "삭제":
            result = await utils.data.commit(f"DELETE FROM `blacklist` WHERE `id` = '{id}'")
            if result == "SUCCESS":
                await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
        else:
            await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 블랙 < 추가 / 삭제 > < ID > [ 사유 ]`(이)가 올바른 명령어에요!")

def setup(miya):
    miya.add_cog(Development(miya)) 
