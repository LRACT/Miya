import aiohttp
import discord
from discord.ext import commands
from utils import koreanbots

class General(commands.Cog):
    def __init__(self, miya):
        self.miya = miya

    @commands.command(name="핑")
    async def _ping(self, ctx):
        await ctx.send(f"{ctx.author.mention} Pong! `{round(self.miya.latency * 1000)}ms`")
    
    @commands.command(name="봇정보")
    async def _miyainfo(self, ctx):
        heart = await koreanbots.get_rank()
        e = discord.Embed(title="미야 서버(봇) 정보", description=f"순위: {heart}\n<:cs_settings:659355468992610304> CPU : Xeon E3-1280 v6\n<:rem:727570626407301241> Memory : DDR4 16GB (삼성 8기가 2개)\n<:ssd:727570626092728474> Storage : SAMSUNG 860 EVO (500GB)\n<:cs_id:659355469034422282> 프로필 출처 : [보러 가기](https://pixiv.net/artworks/82178761)\n<:cs_leave:659355468803866624> 서버 갯수 : {len(self.miya.guilds)}개", color=0xAFFDEF)
        await ctx.send(ctx.author.mention, embed=e)

    @commands.command(name="한강")
    async def _hangang(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('http://hangang.dkserver.wo.tc/') as r:
                response = await r.json()
                await ctx.send(f"한강온도는 {response['temp']}") # 알아서 임베드 넣어라
        

def setup(miya):
    miya.add_cog(General(miya))