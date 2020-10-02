import discord
from discord.ext import commands
import aiosqlite
import datetime
import os
import aiohttp
import ast
import asyncio
from pytz import utc, timezone
from utils import data, hook

def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

class dev(commands.Cog, name="개발"):
    def __init__(self, miya):
        self.miya = miya

    @commands.command(name="모듈")
    @commands.is_owner()
    async def module_management(self, ctx, *args):
        """
        미야야 모듈 < 활성화 / 비활성화 / 재시작 > < 모듈 >


        미야에 등록된 모듈을 관리합니다.
        """
        if not args:
            return
        else:
            if args[0] == "재시작":
                try:
                    self.miya.reload_extension(f'modules.{args[1]}')
                except Exception as e:
                    await ctx.send(f"{ctx.author.mention} 모듈 다시 시작 실패.\n{e}")
                else:
                    await ctx.message.add_reaction("<:cs_yes:659355468715786262>")

            if args[0] == "활성화":
                try:
                    self.miya.load_extension(f'modules.{args[1]}')
                except Exception as e:
                    await ctx.send(f"{ctx.author.mention} 모듈 활성화 실패.\n{e}")
                else:
                    await ctx.message.add_reaction("<:cs_yes:659355468715786262>")

            if args[0] == "비활성화":
                try:
                    self.miya.unload_extension(f'modules.{args[1]}')
                except Exception as e:
                    await ctx.send(f"{ctx.author.mention} 모듈 비활성화 실패.\n{e}")
                else:
                    await ctx.message.add_reaction("<:cs_yes:659355468715786262>")

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
            'aiosqlite': aiosqlite,
            'asyncio': asyncio,
            'datetime': datetime,
            'aiohttp': aiohttp,
            'os': os
        }
        evaluating = await ctx.send(f"<a:cs_wait:659355470418411521> {ctx.author.mention} 잠시만 기다려주세요... API와 DB에서 당신의 요청을 처리하고 있어요!")
        try:
            exec(compile(parsed, filename="<ast>", mode="exec"), env)
            result = (await eval(f"{fn_name}()", env))    
        except Exception as error:
            await evaluating.edit(content=f"<:cs_protect:659355468891947008> {ctx.author.mention} - 구문 실행 실패;\n```{error}```")
        else:
            if result is not None:
                await evaluating.edit(content=f"<:cs_console:659355468786958356> {ctx.author.mention} - 구문 실행을 성공적으로 마쳤어요.\n```{result}```")
            else:
                await evaluating.edit(content=f"<:cs_console:659355468786958356> {ctx.author.mention} - 구문 실행을 성공적으로 마쳤지만, 반환된 값이 없어요.")

    @commands.command(name="블랙")
    @commands.is_owner()
    async def add_blacklist(self, ctx, user: discord.User, *, reason):
        """
        미야야 블랙 < 유저 >


        지목한 유저를 블랙리스트에 추가합니다.
        블랙리스트에 추가되면 미야를 사용할 수 없습니다.
        """
        await ctx.message.delete()
        uploading = await ctx.send(f"<a:cs_wait:659355470418411521> {ctx.author.mention} 잠시만 기다려주세요... DB에서 당신의 요청을 처리하고 있어요!")
        KST = timezone('Asia/Seoul')
        now = datetime.datetime.utcnow()
        time = utc.localize(now).astimezone(KST)
        times = time.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
        await data.insert('blacklist', 'user, admin, reason, datetime', f"{user.id}, {ctx.author.id}, '{reason}', '{times}'")
        await uploading.edit(content=f"<:cs_yes:659355468715786262> {ctx.author.mention} {user}님을 블랙리스트에 추가했어요!")
    
    @commands.command(name="언블랙")
    @commands.is_owner()
    async def remove_blacklist(self, ctx, user: discord.User):
        """
        미야야 언블랙 < 유저 >


        지목한 유저를 블랙리스트에서 제거합니다.
        """
        await ctx.message.delete()
        uploading = await ctx.send(f"<a:cs_wait:659355470418411521> {ctx.author.mention} 잠시만 기다려주세요... DB에서 당신의 요청을 처리하고 있어요!")
        await data.delete("blacklist", 'user', user.id)
        await uploading.edit(content=f"<:cs_yes:659355468715786262> {ctx.author.mention} {user}님을 블랙리스트에서 제거했어요!")
    
    @commands.command(name="강제등록")
    @commands.is_owner()
    async def force_register(self, ctx, *args):
        guild = self.miya.get_guild(int(args[0]))
        if guild is not None:
            uploading = await ctx.send(f"<a:cs_wait:659355470418411521> {ctx.author.mention} 잠시만 기다려주세요... DB에서 당신의 요청을 처리하고 있어요!")
            g_result = await data.insert('guilds', 'guild, eventLog, muteRole, linkFiltering, warn_kick', f'{guild.id}, 1234, 1234, "false", 0')
            default_join_msg = "{member}님 **{guild}**에 오신 것을 환영해요! 현재 인원 : {count}명"
            default_quit_msg = "{member}님 잘가세요.. 현재 인원 : {count}명"
            m_result = await data.insert('memberNoti', 'guild, channel, join_msg, remove_msg', f'{guild.id}, 1234, "{default_join_msg}", "{default_quit_msg}"')
            if g_result == "SUCCESS" and m_result == "SUCCESS":
                await hook.send(f"Guild registered :: {guild.name} ( {guild.id} )", "미야 Terminal", self.miya.user.avatar_url)
                print(f"Guild registered :: {guild.name} ( {guild.id} )")
                await uploading.edit(content=f"<:cs_yes:659355468715786262> {ctx.author.mention} {guild.name}, 등록이 완료되었습니다.")
            else:
                await hook.send(f"Guild register failed :: {guild.name} ( {guild.id} )\n{guild.id} guild Table :: {g_result}\n{guild.id} memberNoti Table :: {m_result}", "미야 Terminal", self.miya.user.avatar_url)
                print(f"Guild register failed :: {guild.name} ( {guild.id} )\n{guild.id} guild Table :: {g_result}\n{guild.id} memberNoti Table :: {m_result}")
                await uploading.edit(content=f"<:cs_no:659355468816187405> {ctx.author.mention} 서버 등록 도중에 오류가 발생했습니다.")

def setup(miya):
    miya.add_cog(dev(miya)) 
