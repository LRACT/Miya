import discord
from discord.ext import commands
import typing
import utils
import locale
import datetime
locale.setlocale(locale.LC_ALL, '')

class Development(commands.Cog, name="개발"):
    def __init__(self, miya):
        self.miya = miya

    def is_manager():
        return commands.check(utils.get.mgr)

    @commands.command(name="모듈")
    @commands.is_owner()
    async def module_management(self, ctx, todo, *, module):
        """
        미야야 모듈 < 활성화 / 비활성화 / 재시작 > < 모듈 >


        미야에게 등록된 모듈을 관리합니다.
        """
        if todo == "재시작":
            try:
                self.miya.reload_extension(module)
            except Exception as e:
                await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} {module} 모듈을 다시 시작할 수 없었어요.\n`{e}`")
            else:
                await ctx.message.add_reaction("<:cs_reboot:659355468791283723>")
        elif todo == "활성화":
            try:
                self.miya.load_extension(module)
            except Exception as e:
                await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} {module} 모듈을 활성화할 수 없었어요.\n`{e}`")
            else:
                await ctx.message.add_reaction("<:cs_on:659355468682231810>")
        elif todo == "비활성화":
            try:
                self.miya.unload_extension(module)
            except Exception as e:
                await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} {module} 모듈을 비활성화할 수 없었어요.\n`{e}`")
            else:
                await ctx.message.add_reaction("<:cs_off:659355468887490560>")
        else:
            await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 모듈 < 활성화 / 비활성화 / 재시작 > < 모듈 >`(이)가 올바른 명령어에요!")


    @commands.command(name="제한")
    @is_manager()
    async def _black_word(self, ctx, todo, *, word):
        """
        미야야 제한 < 추가 / 삭제 > < 단어 >
        
        
        특정 단어 사용 시 미야 사용이 제한되게 합니다.
        """
        if todo == "추가":
            result = await utils.data.commit(f"INSERT INTO `forbidden`(`word`) VALUES('{word}')")
            if result == "SUCCESS":
                await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
                await utils.webhook.blacklist(f"Forbidden Word Added By {ctx.author} - {word}", "Word Limit Notify", self.miya.user.avatar_url)
            else:
                await ctx.message.add_reaction("<:cs_no:659355468816187405>")
        elif todo == "삭제":
            result = await utils.data.commit(f"DELETE FROM `forbidden` WHERE `word` = '{word}'")
            if result == "SUCCESS":
                await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
                await utils.webhook.blacklist(f"Forbidden Word Removed By {ctx.author} - {word}", "Word Limit Notify", self.miya.user.avatar_url)
            else:
                await ctx.message.add_reaction("<:cs_no:659355468816187405>")
        else:
            await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 제한 < 추가 / 삭제 > < 단어 >`(이)가 올바른 명령어에요!")


    @commands.command(name="블랙")
    @is_manager()
    async def blacklist_management(self, ctx, todo, id, *, reason: typing.Optional[str] = "사유가 지정되지 않았습니다."):
        """
        미야야 블랙 < 추가 / 삭제 > < ID > [ 사유 ]

        
        ID를 통해 유저나 서버의 블랙리스트를 관리합니다.
        """
        date = datetime.datetime.utcnow()
        time = await utils.get.kor_time(date)
        if todo == "추가":
            result = await utils.data.commit(f"INSERT INTO `blacklist`(`id`, `reason`, `admin`, `datetime`) VALUES('{id}', '{reason}', '{ctx.author.id}', '{time}')")
            if result == "SUCCESS":
                await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
                await utils.webhook.blacklist(f"Blacklisted ( Administrator ) : {id} - {reason}", "Blacklist Notify", self.miya.user.avatar_url)
            else:
                await ctx.message.add_reaction("<:cs_no:659355468816187405>")
        elif todo == "삭제":
            result = await utils.data.commit(f"DELETE FROM `blacklist` WHERE `id` = '{id}'")
            if result == "SUCCESS":
                await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
            else:
                await ctx.message.add_reaction("<:cs_no:659355468816187405>")
        else:
            await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 블랙 < 추가 / 삭제 > < ID > [ 사유 ]`(이)가 올바른 명령어에요!")
   
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
            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 서버를 발견하지 못했어요.")

def setup(miya):
    miya.add_cog(Development(miya)) 
