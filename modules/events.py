import discord
from discord.ext import commands
import json
import aiohttp
from utils import data
from lib import config
import datetime


class handler(commands.Cog, name="이벤트 리스너"):
    def __init__(self, miya):
        self.miya = miya

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.miya.user)
        print(self.miya.user.id)
        await self.miya.change_presence(
            status=discord.Status.idle, activity=discord.Game("'미야야 도움'이라고 말해보세요!")
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
        elif isinstance(error, commands.NotOwner):
            await ctx.send(f"{ctx.author.mention} 해당 명령어는 미야 관리자에 한해 사용이 제한됩니다.")
        else:
            print(error)
            await ctx.send(f"{ctx.author.mention} 오류 발생; 이 현상이 계속될 경우 Discord 지원 서버 ( https://discord.gg/mdgaSjB )로 문의해주세요.")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"Added to {guild.id}")
        default_join_msg = "{member}님 {guild}에 오신 것을 환영해요! 현재 인원 : {count}"
        default_quit_msg = "{member}님 잘가세요.. 현재 인원 : {count}"
        row = await data.load('guilds', 'guild', guild.id)
        if row is None:
            result = await data.insert('guilds', "guild, announce, muteRole", f'{guild.id}, 1234, 1234')
            result2 = await data.insert('memberNoti', 'guild, channel, join_msg, remove_msg', f'{guild.id}, 1234, "{default_join_msg}", "{default_quit_msg}"')
            result3 = await data.insert('eventLog', 'guild, channel, events', f"{guild.id}, 1234, None")
            if result == "SUCCESS" and result2 == "SUCCESS" and result3 == "SUCCESS":
                print(f"Guild registered :: {guild.name} ( {guild.id} )")
            else:
                print(f"{guild.id} guild Table :: {result}")
                print(f"{guild.id} memberNoti Table :: {result2}")
                print(f"{guild.id} eventLog Table :: {result3}")
                try:
                    await guild.owner.send(f"{guild.owner.mention} 서버 등록 도중에 오류가 발생했습니다. 봇을 다시 초대해주세요.\n계속해서 이런 현상이 발생한다면 https://github.com/LRACT/Miya 에 이슈를 남겨주세요.")
                except:
                    print(f"Cannot send DM to guild ( {guild.id} ) owner.")
                else:
                    print(f"Successfully sent error msg to guild ( {guild.id} ) owner.")
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        print(f"Removed from {guild.name} ( {guild.id} )")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        #result = await data.load('')
        if member.bot == False:
            value = await data.load(table="memberNoti", find_column="guild", find_value=member.guild.id)
            if value is None:
                return
            else:
                channel = member.guild.get_channel(int(value[1]))
                if channel is not None and value[2] != "":
                    msg = value[2].replace("{member}", str(member.mention))
                    msg = msg.replace("{guild}", str(member.guild.name))
                    msg = msg.replace("{count}", str(member.guild.member_count))
                    await channel.send(msg)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.bot == False:
            value = await data.load(table="memberNoti", find_column="guild", find_value=member.guild.id)
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
