import discord
from discord.ext import commands
import aiosqlite
import datetime
import os
import aiohttp
import ast
import asyncio
from pytz import utc, timezone
from utils import data

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
        try:
            exec(compile(parsed, filename="<ast>", mode="exec"), env)
            result = (await eval(f"{fn_name}()", env))    
        except Exception as error:
            await ctx.send(f"<:cs_protect:659355468891947008> {ctx.author.mention} - 구문 실행 실패;\n```{error}```")
        else:
            if result is not None:
                await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} - 구문 실행을 성공적으로 마쳤어요.\n```{result}```")
            else:
                await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} - 구문 실행을 성공적으로 마쳤지만, 반환된 값이 없어요.")

    @commands.command(name="블랙")
    @commands.is_owner()
    async def add_blacklist(self, ctx, user: discord.User, *, reason):
        """
        미야야 블랙 < 유저 >


        지목한 유저를 블랙리스트에 추가합니다.
        블랙리스트에 추가되면 미야를 사용할 수 없습니다.
        """
        KST = timezone('Asia/Seoul')
        now = datetime.datetime.utcnow()
        time = utc.localize(now).astimezone(KST)
        times = time.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
        await data.insert('blacklist', 'user, admin, reason, datetime', f"{user.id}, {ctx.author.id}, '{reason}', '{times}'")
        await ctx.send(f"<:cs_yes:659355468715786262> {ctx.author.mention} {user}님을 블랙리스트에 추가했어요!")
    
    @commands.command(name="언블랙")
    @commands.is_owner()
    async def remove_blacklist(self, ctx, user: discord.User):
        """
        미야야 언블랙 < 유저 >


        지목한 유저를 블랙리스트에서 제거합니다.
        """
        await data.delete("blacklist", 'user', user.id)
        await ctx.send(f"<:cs_yes:659355468715786262> {ctx.author.mention} {user}님을 블랙리스트에서 제거했어요!")

def setup(miya):
    miya.add_cog(dev(miya)) 
