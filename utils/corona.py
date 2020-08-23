import aiohttp
from bs4 import BeautifulSoup

async def corona():
    async with aiohttp.ClientSession() as cs:
        async with cs.get('http://ncov.mohw.go.kr/') as r:
            html = await r.text()

            soup = BeautifulSoup(html, 'lxml')
            data = soup.find('div', class_='liveNum')
            num = data.findAll('span', class_='num')
            corona_info = [corona_num.text for corona_num in num]

            return corona_info # 순서대로 확진자, 완치, 치료, 사망