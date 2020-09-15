import aiohttp
import discord
import asyncio
from discord.ext import commands
from utils import koreanbots
import random

class General(commands.Cog):
    def __init__(self, miya):
        self.miya = miya

    @commands.command(name="핑")
    async def _ping(self, ctx):
        """
        미야야 핑
        
        
        현재 미야의 핑을 출력합니다.
        """ 
        await ctx.send(f"{ctx.author.mention} Pong! `{round(self.miya.latency * 1000)}ms`")
    
    @commands.command(name="초대")
    async def _invite(self, ctx):
        """
        미야야 초대
        
        
        미야의 초대 링크를 표시합니다.
        """
        embed = discord.Embed(title="미야 초대링크", description="[여기](https://discord.com/oauth2/authorize?client_id=720724942873821316&permissions=8&scope=bot)를 클릭하면 초대하실 수 있어요!", color=0x5FE9FF)
        await ctx.send(ctx.author.mention, embed=embed)
    
    @commands.command(name="봇정보")
    async def _miyainfo(self, ctx):
        """
        미야야 봇정보
        
        
        미야의 정보를 표시합니다.
        """
        heart = await koreanbots.get_rank()
        e = discord.Embed(title="미야 서버(봇) 정보", description=f"""
                <:koreanbots:752354740314177568> 봇 순위 : {heart}위
                <:cs_settings:659355468992610304> CPU : Xeon E3-1280 v6
                <:rem:727570626407301241> Memory : DDR4 16GB (삼성 8기가 2개)
                <:ssd:727570626092728474> Storage : SAMSUNG 860 EVO (500GB)
                <:cs_id:659355469034422282> 프로필 출처 : [보러 가기](https://pixiv.net/artworks/82178761)
                <:cs_on:659355468682231810> 리라이트 시작 : 2020년 8월 17일
                <:cs_leave:659355468803866624> 서버 갯수 : {len(self.miya.guilds)}개""", 
            color=0x5FE9FF
        )
        await ctx.send(ctx.author.mention, embed=e)

    @commands.command(name="한강")
    async def _hangang(self, ctx):
        """
        미야야 한강


        현재 한강의 수온을 출력합니다.
        """
        async with aiohttp.ClientSession() as cs:
            async with cs.get("http://hangang.dkserver.wo.tc") as r:
                response = await r.json(content_type=None) 
                embed = discord.Embed(description=f'현재 한강의 온도는 `{response["temp"]}`도에요!\n`측정: {(response["time"]).split(" ")[0]}`', color=0x5FE9FF)
                embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.name)
                temp = None
                if "." in response["temp"]:
                    temp = int(response["temp"].split(".")[0])
                else:
                    temp = int(response["temp"])
                    
                if temp > 15: 
                    embed.set_footer(text="거 수온이 뜨듯하구먼!")
                else:
                    embed.set_footer(text="거 이거 완전 얼음장이구먼!")
                await ctx.send(ctx.author.mention, embed=embed)

    @commands.command(name="골라", aliases=["골라줘"])
    async def _select(self, ctx, *args):
        """ 
        미야야 골라 < 단어1 > < 단어2 > [ 단어3 ] ...
        
        
        미야가 단어 중 랜덤하게 하나를 선택해줍니다.
        """
        select = random.choice(args)
        embed = discord.Embed(description=select, color=0x5FE9FF)
        embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.name) 
        await ctx.send(embed=embed)

def setup(miya):
    miya.add_cog(General(miya))
