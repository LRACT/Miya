import aiohttp
from bs4 import BeautifulSoup
import locale
from lib import config
locale.setlocale(locale.LC_ALL, '')

async def team(user_id, app): 
    t_members = app.team.members
    owner = False
    for t in t_members:
        if t.id == user_id:
            owner = True
    
    return owner

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
    words = config.Forbidden.split(" ")
    for word in words:
        if word in msg.content:
            forbidden = True
            banned = word
    
    value = [forbidden, banned]
    return value