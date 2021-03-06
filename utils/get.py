import aiohttp
from bs4 import BeautifulSoup
import locale
from lib import config
import datetime
import aiomysql
from discord.ext import commands
from pytz import timezone, utc
from utils import exc, data
locale.setlocale(locale.LC_ALL, '')

async def mgr(ctx):
    rows = await data.fetch("SELECT `manager` FROM `miya`")
    mgrs = rows[0][0].split(" ")
    a = None
    for m in mgrs:
        if ctx.author.id == int(m):
            return True
    return False 

async def kor_time(date):
    KST = timezone('Asia/Seoul')
    now = date
    abc = utc.localize(now).astimezone(KST)
    time = abc.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
    return time

async def hangang():
    async with aiohttp.ClientSession() as cs:
        async with cs.get("http://hangang.dkserver.wo.tc") as r:
            response = await r.json(content_type=None)
            temp = None
            time = (response["time"]).split(" ")[0]
            if "." in response["temp"]:
                temp = int(response["temp"].split(".")[0])
            else:
                temp = int(response["temp"])
    
    return [temp, time]

async def corona():
    async with aiohttp.ClientSession() as cs:
        async with cs.get('http://ncov.mohw.go.kr/') as r:
            html = await r.text()

            soup = BeautifulSoup(html, 'lxml')
            data = soup.find('div', class_='liveNum')
            num = data.findAll('span', class_='num')
            corona_info = [corona_num.text for corona_num in num]

            return corona_info # 순서대로 확진자, 완치, 치료, 사망

async def check(ctx, miya):
    mgr = await mgr(ctx)

    reason, admin, time, banned, forbidden = None, None, None, None, None
    words = await data.fetch("SELECT * FROM `forbidden`")
    for word in words:
        if word[0] in msg.content:
            forbidden = True
            banned = word[0]
    rows = await data.fetch(f"SELECT * FROM `blacklist` WHERE `id` = '{ctx.author.id}'")
    if rows:
        if mgr is not True:
            reason = rows[0][1]
            admin = miya.get_user(int(rows[0][2]))
            time = rows[0][3]
            await webhook.terminal(f"Blocked User >\nUser - {ctx.author} ({ctx.author.id})\nContent - {ctx.message.content}\nGuild - {ctx.guild.name} ({ctx.guild.id})", "명령어 처리 기록", miya.user.avatar_url)
        else:
            await ctx.send("당신은 차단되었지만, 관리 권한으로 명령어를 실행했습니다.")
            await webhook.terminal(f"Manager Bypassed >\nUser - {ctx.author} ({ctx.author.id})\nContent - {ctx.message.content}\nGuild - {ctx.guild.name} ({ctx.guild.id})", "명령어 처리 기록", miya.user.avatar_url)
            return True
    elif forbidden is True:
        if mgr is not True:
            reason = f"부적절한 언행 **[Auto]** - {banned}"
            admin = miya.user
            time = await kor_time(datetime.datetime.utcnow())
            await data.commit(f"INSERT INTO `blacklist`(`id`, `reason`, `admin`, `datetime`) VALUES('{ctx.author.id}', '{reason}', '{admin.id}', '{time}')")
            await webhook.blacklist(f"New Block >\nVictim - {ctx.author.id}\nAdmin - {admin} ({admin.id})\nReason - {reason}", "제한 기록", miya.user.avatar_url)
            await webhook.terminal(f"Forbidden >\nUser - {ctx.author} ({ctx.author.id})\nContent - {ctx.message.content}\nGuild - {ctx.guild.name} ({ctx.guild.id})", "명령어 처리 기록", miya.user.avatar_url)
        else:
            await ctx.send("당신은 차단되었지만, 관리 권한으로 명령어를 실행했습니다.")
            await webhook.terminal(f"Manager Bypassed >\nUser - {ctx.author} ({ctx.author.id})\nContent - {ctx.message.content}\nGuild - {ctx.guild.name} ({ctx.guild.id})", "명령어 처리 기록", miya.user.avatar_url)
            return True
    else:
        await webhook.terminal(f"Processed >\nUser - {ctx.author} ({ctx.author.id})\nContent - {ctx.message.content}\nGuild - {ctx.guild.name} ({ctx.guild.id})", "명령어 처리 기록", miya.user.avatar_url)
        return True
    embed = discord.Embed(
        title=f"이런, {ctx.author}님은 차단되셨어요.",
        description=f"""
차단에 관해서는 지원 서버를 방문해주세요.
사유 : {reason}
관리자 : {admin}
차단 시각 : {time}
        """,
        timestamp=datetime.datetime.utcnow(),
        color=0xFF3333
    )
    embed.set_author(name="이용 제한", icon_url=miya.user.avatar_url)   
    raise exc.Forbidden(embed, ctx)
