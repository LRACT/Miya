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

    @commands.command(name="모듈")
    @commands.is_owner()
    async def module_management(self, ctx, *args):
        """
        미야야 모듈 < 활성화 / 비활성화 / 재시작 > < 모듈 >


        미야에 등록된 모듈을 관리합니다.
        """
        if not args or len(args) < 2:
            await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 모듈 < 활성화 / 비활성화 / 재시작 > < 모듈 >`(이)가 올바른 명령어에요!")
        else:
            if args[0] == "재시작":
                try:
                    self.miya.reload_extension(f'modules.{args[1]}')
                except Exception as e:
                    await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} {args[1]} 모듈을 다시 시작할 수 없었습니다.\n`{e}``")
                else:
                    await ctx.message.add_reaction("<:cs_reboot:659355468791283723>")
            elif args[0] == "활성화":
                try:
                    self.miya.load_extension(f'modules.{args[1]}')
                except Exception as e:
                    await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} {args[1]} 모듈을 활성화할 수 없었습니다.\n`{e}``")
                else:
                    await ctx.message.add_reaction("<:cs_on:659355468682231810>")
            elif args[0] == "비활성화":
                try:
                    self.miya.unload_extension(f'modules.{args[1]}')
                except Exception as e:
                    await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} {args[1]} 모듈을 비활성화할 수 없었습니다.\n`{e}``")
                else:
                    await ctx.message.add_reaction("<:cs_off:659355468887490560>")
            else:
                await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 모듈 < 활성화 / 비활성화 / 재시작 > < 모듈 >`(이)가 올바른 명령어에요!")

    # Thanks to nitros12
    @commands.command(name="실행")
    @commands.is_owner()
    async def evaluate(self, ctx, *, cmd):
        """
        미야야 실행 < 코드 >


        작성한 코드를 EVAL로 실행합니다.
        """
        fn_name = "_eval_expr"
        cmd = cmd.strip("` ")
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
        body = f"async def {fn_name}():\n{cmd}"
        parsed = ast.parse(body)
        body = parsed.body[0].body
        insert_returns(body)

        env = {
            'miya': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__,
            'aiomysql': aiomysql,
            'asyncio': asyncio,
            'datetime': datetime,
            'aiohttp': aiohttp,
            'os': os
        }
        working = await ctx.send(f"<a:cs_wait:659355470418411521> {ctx.author.mention} 잠시만 기다려주세요... API와 DB에서 당신의 요청을 처리하고 있어요!")
        try:
            exec(compile(parsed, filename="<ast>", mode="exec"), env)
            result = (await eval(f"{fn_name}()", env))    
        except Exception as error:
            await working.edit(content=f"<:cs_protect:659355468891947008> {ctx.author.mention} - 구문 실행 실패;\n```{error}```")
        else:
            if result is not None:
                await working.edit(content=f"<:cs_console:659355468786958356> {ctx.author.mention} - 구문 실행을 성공적으로 마쳤어요.\n```{result}```")
            else:
                await working.edit(content=f"<:cs_console:659355468786958356> {ctx.author.mention} - 구문 실행을 성공적으로 마쳤지만, 반환된 값이 없어요.")

    @commands.command(name="블랙")
    @commands.is_owner()
    async def blacklist_management(self, ctx, todo, what, identity: int, *, reason: typing.Optional[str] = "사유가 지정되지 않았습니다."):
        """
        미야야 블랙 < 추가 / 삭제 > < 서버 / 유저 > < ID > [ 사유 ]

        
        ID를 통해 유저나 서버의 블랙리스트를 관리합니다.
        """
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
                        await guild.leave()
                    else:
                        await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 블랙리스트 삭제에 실패했어요. 사유 : {result}")
                else:
                    await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 블랙리스트에 등재되지 않은 ID에요.")
            else:
                await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 블랙 < 추가 / 삭제 > < 서버 / 유저 > < ID > [ 사유 ]`(이)가 올바른 명령어에요!")
        else:
            await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 블랙 < 추가 / 삭제 > < 서버 / 유저 > < ID > [ 사유 ]`(이)가 올바른 명령어에요!")
    
    @commands.command(name="강제등록")
    @commands.is_owner()
    async def force_register(self, ctx, *args):
        """
        미야야 강제등록 < 서버 ID >


        서버의 ID를 통해 서버를 등록합니다.
        """
        guild = self.miya.get_guild(int(args[0]))
        if guild is not None:
            working = await ctx.send(f"<a:cs_wait:659355470418411521> {ctx.author.mention} 잠시만 기다려주세요... API와 DB에서 당신의 요청을 처리하고 있어요!")
            g_result = await data.insert('guilds', '`guild`, `eventLog`, `muteRole`, `linkFiltering`, `warn_kick`', f'"{guild.id}", "1234", "1234", "false", "0"')
            default_join_msg = "{member}님 **{guild}**에 오신 것을 환영해요! 현재 인원 : {count}명"
            default_quit_msg = "{member}님 잘가세요.. 현재 인원 : {count}명"
            m_result = await data.insert('memberNoti', '`guild`, `channel`, `join_msg`, `remove_msg`', f'"{guild.id}", "1234", "{default_join_msg}", "{default_quit_msg}"')
            await webhook.terminal(f"Force guild register :: {guild.name} ( {guild.id} )\n{guild.id} guilds Table :: {g_result}\n{guild.id} memberNoti Table :: {m_result}", "미야 Terminal", self.miya.user.avatar_url)
            print(f"Force guild register :: {guild.name} ( {guild.id} )\n{guild.id} guilds Table :: {g_result}\n{guild.id} memberNoti Table :: {m_result}")
            await working.edit(content=f"<:cs_yes:659355468715786262> {ctx.author.mention} {guild.name} 서버를 DB에 등록 시도한 결과,\nguilds 테이블에서 `{g_result}` 결과를 제출했고,\nmemberNoti 테이블에서 `{m_result}` 결과를 제출했습니다.")
        else:
            await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 강제등록 < 서버 ID >`(이)가 올바른 명령어에요!")
    
    @commands.command(name="응답")
    @commands.is_owner()
    async def answer(self, ctx, sender: discord.User, *, response):
        """
        미야야 응답 < 유저 > < 할말 >


        해당 유저에게 피드백에 대한 응답을 회신합니다.
        """
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
                    await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 해당 유저가 DM을 막아놓은 것 같아요. 전송에 실패했어요.")
            else:
                await msg.delete() 
    
    @commands.command(name="경고")
    @commands.is_owner()
    @commands.has_permissions(manage_messages=True)
    async def _warnings(self, ctx, what, member: discord.Member, *, reason: typing.Optional[str] = None):
        """
        미야야 경고 < 추가 / 삭제 / 초기화 / 목록 > < @유저 > [ 사유 ]


        유저의 경고를 관리합니다.
        """
        if what == "추가":
            result = await data.insert('warns', "guild, user, reason", f"{ctx.guild.id}, {member.id}, '{reason}'")
            if result == "SUCCESS":
                await ctx.send(f":warning: {ctx.author.mention} {member.mention}님의 경고를 1회 추가했어요.\n사유 : {reason}")
            else:
                print(f"Warn give failed. warns Result : {result}")
                await ctx.send(f":warning: {ctx.author.mention} 오류 발생; 이 오류가 지속될 경우 Discord 지원 서버로 문의해주세요. https://discord.gg/mdgaSjB")
        elif what == "삭제":
            result = await data.delete('warns', "guild, user, reason", f"{ctx.guild.id}, {member.id}, '{reason}'")
            if result == "SUCCESS":
                await ctx.send(f":warning: {ctx.author.mention} {member.mention}님의 경고를 1회 추가했어요.\n사유 : {reason}")
            else:
                print(f"Warn give failed. warns Result : {result}")
                await ctx.send(f":warning: {ctx.author.mention} 오류 발생; 이 오류가 지속될 경우 Discord 지원 서버로 문의해주세요. https://discord.gg/mdgaSjB")

def setup(miya):
    miya.add_cog(Development(miya)) 
