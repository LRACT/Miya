import aiohttp
from bs4 import BeautifulSoup
import locale
from lib import config
import datetime
import aiomysql
from utils import exc
from pytz import timezone, utc
locale.setlocale(locale.LC_ALL, '')

async def mgr(ctx):
    o = await aiomysql.connect(
        host=config.MySQL['host'],
        port=config.MySQL['port'],
        user=config.MySQL['username'],
        password=config.MySQL['password'],
        db=config.MySQL['database'],
        autocommit=True
    )
    c = await o.cursor()
    await c.execute("SELECT `manager` FROM `miya`")
    rows = await c.fetchall()
    mgrs = rows[0][0].split(" ")
    for m in mgrs:
        if ctx.author.id == int(m):
            return True
    raise exc.No_management

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

async def filter(msg):
    forbidden = False
    banned = None
    o = await aiomysql.connect(
        host=config.MySQL['host'],
        port=config.MySQL['port'],
        user=config.MySQL['username'],
        password=config.MySQL['password'],
        db=config.MySQL['database'],
        autocommit=True
    )
    c = await o.cursor()
    await c.execute("SELECT * FROM `forbidden`")
    rows = await c.fetchall()
    for row in rows:
        if row[0] in msg.content:
            forbidden = True
            banned = row[0]
    
    value = [forbidden, banned]
    return value

async def processing(ctx):
    f = await filter(ctx.message)
    rows = await data.fetch(f"SELECT * FROM `blacklist` WHERE `id` = '{ctx.author.id}'")
    if rows:
        admin = miya.get_user(int(rows[0][2]))
        embed = discord.Embed(
            title=f"이런, {ctx.author}님은 차단되셨어요.",
            description=f"""
차단에 관해서는 지원 서버를 방문해주세요.
사유 : {rows[0][1]}
관리자 : {admin}
차단 시각 : {rows[0][3]}
            """,
            timestamp=datetime.datetime.utcnow(),
            color=0xFF3333
        )
        await webhook.terminal(f"Cancelled (Block) >\nUser - {ctx.author} ({ctx.author.id})\nContent - {ctx.message.content}\nGuild - {ctx.guild.name} ({ctx.guild.id})", "명령어 처리 기록", miya.user.avatar_url)
        raise exc.Forbidden(embed, ctx)
    elif f[0] == True:
        admin = miya.user
        time = await kor_time(datetime.datetime.utcnow())
        embed = discord.Embed(
            title=f"이런, {ctx.author}님은 차단되셨어요.",
            description=f"""
차단에 관해서는 지원 서버를 방문해주세요.
사유 : 봇 사용 도중 부적절한 언행 **[Auto]** - {f[1]}
관리자 : {admin}
차단 시각 : {time}
            """,
            timestamp=datetime.datetime.utcnow(),
            color=0xFF3333
        )
        await webhook.terminal(f"Cancelled (Auto) >\nUser - {ctx.author} ({ctx.author.id})\nContent - {ctx.message.content}\nGuild - {ctx.guild.name} ({ctx.guild.id})", "명령어 처리 기록", miya.user.avatar_url)
        raise exc.Forbidden(embed, ctx)
    else:
        await webhook.terminal(f"Processed >\nUser - {ctx.author} ({ctx.author.id})\nContent - {ctx.message.content}\nGuild - {ctx.guild.name} ({ctx.guild.id})", "명령어 처리 기록", miya.user.avatar_url)
        return True
