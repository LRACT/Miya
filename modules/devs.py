import discord
from discord.ext import commands
import aiomysql
import datetime
import os
import aiohttp
import ast
import asyncio
from pytz import utc, timezone
from utils import data, webhook
import typing
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

    @commands.command(name="블랙")
    @commands.is_owner()
    async def blacklist_management(self, ctx, todo, what, identity: int, *, reason: typing.Optional[str] = "사유가 지정되지 않았습니다."):
        """
        미야야 블랙 < 추가 / 삭제 > < 서버 / 유저 > < ID > [ 사유 ]

        
        ID를 통해 유저나 서버의 블랙리스트를 관리합니다.
        """
        await ctx.message.delete()
        KST = timezone('Asia/Seoul')
        now = datetime.datetime.utcnow()
        time = utc.localize(now).astimezone(KST)
        time = time.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
        if todo == "추가":
            if what == "서버":
                guild = self.miya.get_guild(identity)
                if guild is not None:
                    result = await data.load('blacklist', 'id', guild.id)
                    if result is None:
                        result = await data.insert('blacklist', '`id`, `admin`, `reason`, `datetime`', f"'{guild.id}', '{ctx.author.id}', '{reason}', '{time}'")
                        if result == "SUCCESS":
                            await ctx.send(f"<:cs_yes:659355468715786262> {ctx.author.mention} 서버 {guild.name}(을)를 블랙리스트에 추가했어요!")
                            await guild.leave()
                        else:
                            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 블랙리스트 추가에 실패했어요. 사유 : {result}")
                    else:
                        await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 이미 블랙리스트에 추가된 서버에요.")
                else:
                    await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 블랙리스트에 추가하려는 서버를 찾지 못했어요.")
            elif what == "유저":
                user = self.miya.get_user(identity)
                if user is not None:
                    result = await data.load('blacklist', 'id', user.id)
                    if result is None:
                        result = await data.insert('blacklist', '`id`, `admin`, `reason`, `datetime`', f"'{user.id}', '{ctx.author.id}', '{reason}', '{time}'")
                        if result == "SUCCESS":
                            await ctx.send(f"<:cs_yes:659355468715786262> {ctx.author.mention} {user}님을 블랙리스트에 추가했어요!")
                        else:
                            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 블랙리스트 추가에 실패했어요. 사유 : {result}")
                    else:
                        await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 이미 블랙리스트에 추가된 유저에요.")
                else:
                    await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 블랙리스트에 추가하려는 유저를 찾지 못했어요.")
            else:
                await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 블랙 < 추가 / 삭제 > < 서버 / 유저 > < ID > [ 사유 ]`(이)가 올바른 명령어에요!")
        elif todo == "삭제":
            if what == "서버" or what == "유저":
                result = await data.load('blacklist', 'id', identity)
                if result is not None:
                    result = await data.delete('blacklist', 'id', identity)
                    if result == "SUCCESS":
                        await ctx.send(f"<:cs_yes:659355468715786262> {ctx.author.mention} {identity} ID를 블랙리스트에서 삭제했어요!")
                    else:
                        await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 블랙리스트 삭제에 실패했어요. 사유 : {result}")
                else:
                    await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 블랙리스트에 등재되지 않은 ID에요.")
            else:
                await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 블랙 < 추가 / 삭제 > < 서버 / 유저 > < ID > [ 사유 ]`(이)가 올바른 명령어에요!")
        else:
            await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 블랙 < 추가 / 삭제 > < 서버 / 유저 > < ID > [ 사유 ]`(이)가 올바른 명령어에요!")

    @commands.command(name="응답", aliases=["답변"])
    @commands.is_owner()
    async def answer(self, ctx, sender: discord.User, *, response):
        """
        미야야 응답 < 유저 > < 할말 >


        해당 유저에게 피드백에 대한 응답을 회신합니다.
        """
        await ctx.message.delete()
        KST = timezone('Asia/Seoul')
        now = datetime.datetime.utcnow()
        time = utc.localize(now).astimezone(KST)
        content = "내용 : " + response
        embed = discord.Embed(title="개발자가 답변을 완료했어요!", color=0x95E1F4)
        embed.add_field(name="답변의 내용", value=content, inline=False)
        embed.add_field(name="답변이 완료된 시간", value=time.strftime("%Y년 %m월 %d일 %H시 %M분 %S초"), inline=False)
        embed.set_author(name="문의 및 답변", icon_url=self.miya.user.avatar_url)
        embed.set_footer(text="원하신다면 미야야 피드백 명령어로 계속해서 문의하실 수 있어요!")
        msg = await ctx.send(f"{ctx.author.mention} 이렇게 전송하는 게 맞나요?", embed=embed)
        await msg.add_reaction("<:cs_yes:659355468715786262>")
        await msg.add_reaction("<:cs_no:659355468816187405>")
        def check(reaction, user):
            return reaction.message.id == msg.id and user == ctx.author
        try:
            reaction, user = await self.miya.wait_for('reaction_add', timeout=60, check=check)
        except asyncio.TimeoutError:
            await msg.delete()
        else:
            if str(reaction.emoji) == "<:cs_yes:659355468715786262>":
                try:
                    await msg.delete()
                    await sender.send(sender.mention, embed=embed)
                    await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
                except:
                    await msg.delete()
                    await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 해당 유저가 DM을 막아놓은 것 같아요. 전송에 실패했어요.")
            else:
                await msg.delete() 

def setup(miya):
    miya.add_cog(Development(miya)) 
