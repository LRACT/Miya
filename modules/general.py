import aiohttp
import discord
from discord.ext import commands
from utils import koreanbots
import random

class General(commands.Cog):
    def __init__(self, miya):
        self.miya = miya

    @commands.command(name="핑")
    async def _ping(self, ctx):
        await ctx.send(f"{ctx.author.mention} Pong! `{round(self.miya.latency * 1000)}ms`")
    
    @commands.command(name="봇정보")
    async def _miyainfo(self, ctx):
        heart = await koreanbots.get_rank()
        e = discord.Embed(title="미야 서버(봇) 정보", description=f"""
                <:koreanbots:752354740314177568> 봇 순위 : {heart}위\n
                <:cs_settings:659355468992610304> CPU : Xeon E3-1280 v6\n
                <:rem:727570626407301241> Memory : DDR4 16GB (삼성 8기가 2개)\n
                <:ssd:727570626092728474> Storage : SAMSUNG 860 EVO (500GB)\n
                <:cs_id:659355469034422282> 프로필 출처 : [보러 가기](https://pixiv.net/artworks/82178761)\n
                <:cs_on:659355468682231810> 리라이트 시작 : 2020년 8월 17일\n
                <:cs_leave:659355468803866624> 서버 갯수 : {len(self.miya.guilds)}개""", 
            color=0x5FE9FF
        )
        await ctx.send(ctx.author.mention, embed=e)

    @commands.command(name="한강")
    async def _hangang(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('http://hangang.dkserver.wo.tc/') as r: 
                response = await r.json() 
                embed = discord.Embed(description=f'현재 한강의 온도는 `{response["temp"]}`이에요!', color=0x5FE9FF)
                embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.name) 
                embed.set_footer(text="거 수온이 뜨듯하구먼!")
                await ctx.send(ctx.author.mention, embed=embed)
    
    @commands.command(name="골라", aliases=["골라줘"])
    async def _select(self, ctx, *args):
        select = random.choice(args)
        embed = discord.Embed(description=select, color=0x5FE9FF)
        embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.name) 
        await ctx.send(embed=embed)
        

def setup(miya):
    miya.add_cog(General(miya))