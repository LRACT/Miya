import aiohttp
from bs4 import BeautifulSoup
import locale
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