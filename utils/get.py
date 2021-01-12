import aiohttp
from bs4 import BeautifulSoup
import locale
from lib import config
import datetime
import aiomysql
from pytz import timezone, utc
locale.setlocale(locale.LC_ALL, '')

async def mgr(user):
    o = await aiomysql.connect(
        host=config.MySQL['host'],
        port=config.MySQL['port'],
        user=config.MySQL['username'],
        password=config.MySQL['password'],
        db=config.MySQL['database'],
        autocommit=True
    )
    c = await o.cursor()
    await c.execute("SELECT `manager` FROM `miya` WHERE `botId` = '{miya.id}'")
    rows = await c.fetchall()
    mgrs = rows[0][0].split(" ")
    for m in mgrs:
        if user.id == m:
            return True 

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
