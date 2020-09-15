import discord
from discord.ext import commands
import json
import aiohttp
from utils import data
from lib import config
import datetime


class handler(commands.Cog):
    def __init__(self, miya):
        self.miya = miya

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.miya.user)
        print(self.miya.user.id)
        await self.miya.change_presence(
            status=discord.Status.idle, activity=discord.Game("discord.py 리라이트 중...")
        )
        print("READY")
        uptime_set = await data.update('miya', 'uptime', str(datetime.datetime.now()), 'botId', self.miya.user.id)
        return uptime_set

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            response_msg = None
            url = config.PPBRequest
            headers = {
                "Authorization": config.PPBToken,
                "Content-Type": "application/json",
            }
            async with aiohttp.ClientSession() as cs:
                async with cs.post(
                    url,
                    headers=headers,
                    json={
                        "request": {"query": ctx.message.content.replace("미야야 ", "")}
                    },
                ) as r:
                    response_msg = await r.json()       
            msg = response_msg["response"]["replies"][0]["text"]
            embed = discord.Embed(
                title=msg,
                description=f"[Discord 지원 서버 접속하기](https://discord.gg/mdgaSjB)\n[한국 디스코드 봇 리스트 하트 누르기](https://koreanbots.dev/bots/{self.miya.user.id})",
                color=0x5FE9FF,
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(error)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot == False:
            value = await data.load("memberNoti", "guild", member.guild.id)
            if value is None:
                return
            else:
                channel = member.guild.get_channel(int(value[1]))
                if channel is not None and value[2] != "":
                    msg = value[2].replace("{member}", str(member))
                    msg = msg.replace("{guild}", str(member.guild.name))
                    msg = msg.replace("{count}", str(member.guild.member_count))
                    await channel.send(msg)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.bot == False:
            value = await data.load(member.guild.id, "memberNoti")
            if value is None:
                return
            else:
                channel = member.guild.get_channel(int(value[1]))
                if channel is not None and value[3] != "":
                    msg = value[3].replace("{member}", str(member))
                    msg = msg.replace("{guild}", str(member.guild.name))
                    msg = msg.replace("{count}", str(member.guild.member_count))
                    await channel.send(msg)


def setup(miya):
    miya.add_cog(handler(miya))
