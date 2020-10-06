import discord
from discord.ext import commands
import json
import aiohttp
import asyncio
from utils import data, webhook
from lib import config
import datetime

class Listeners(commands.Cog, name="이벤트 리스너"):
    def __init__(self, miya):
        self.miya = miya

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.miya.user)
        print(self.miya.user.id)        
        print("READY")
        await webhook.terminal(f"{self.miya.user}\n{self.miya.user.id}\n봇이 준비되었습니다.", "미야 Terminal", self.miya.user.avatar_url)
        uptime_set = await data.update('miya', 'uptime', str(datetime.datetime.now()), 'botId', self.miya.user.id)
        await webhook.terminal(f"Uptime Change :: {uptime_set}", "미야 Terminal", self.miya.user.avatar_url)
        print(f"Uptime Change :: {uptime_set}")
        while True:
            for status in config.StatusMessages:
                await self.miya.change_presence(status=discord.Status.online, activity=discord.Game(status.format(len(self.miya.users), len(self.miya.guilds))))
                await asyncio.sleep(5)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        perms = {
            "administrator": "관리자",
            "manage_guild": "서버 관리하기",
            "manage_roles": "역할 관리하기",
            "manage_permissions": "권한 관리하기",
            "manage_channels": "채널 관리하기",
            "kick_members": "멤버 추방하기",
            "ban_members": "멤버 차단하기",
            "manage_nicknames": "별명 관리하기",
            "manage_webhooks": "웹훅 관리하기",
            "manage_messages": "메시지 관리하기"
        }
        if isinstance(error, discord.NotFound):
            return
        elif isinstance(error, discord.Forbidden):
            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 권한 부족 등의 이유로 명령어 실행에 실패했어요...")
        elif isinstance(error, commands.CommandNotFound) or isinstance(error, commands.MissingRole) or isinstance(error, commands.NotOwner):
            response_msg = None
            url = config.PPBRequest
            headers = {
                "Authorization": config.PPBToken,
                "Content-Type": "application/json",
            }
            query = ""
            for q in ctx.message.content.split(" ")[1:]:
                query += f"{q} "
            async with aiohttp.ClientSession() as cs:
                async with cs.post(
                    url,
                    headers=headers,
                    json={
                        "request": {"query": query}
                    },
                ) as r:
                    response_msg = await r.json()  
            msg = response_msg["response"]["replies"][0]["text"]
            await webhook.terminal(f"Sent {query} to Ping Pong builder and got {msg}", "미야 Terminal", self.miya.user.avatar_url)
            print(f"Sent {query} to Ping Pong builder and got {msg}")
            embed = discord.Embed(title=msg, description=f"[Discord 지원 서버 접속하기](https://discord.gg/mdgaSjB)\n[한국 디스코드 봇 리스트 하트 누르기](https://koreanbots.dev/bots/miya)", color=0x5FE9FF)
            embed.set_footer(text="이 기능은 https://pingpong.us/ 를 통해 제작되었습니다.")
            await ctx.send(ctx.author.mention, embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            mp = error.missing_perms
            p = perms[mp[0]]
            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 당신은 이 명령어를 실행할 권한이 없어요.\n해당 명령어를 실행하려면 이 권한을 가지고 계셔야 해요. `{p}`")
        elif isinstance(error, commands.BotMissingPermissions):
            mp = error.missing_perms
            p = perms[mp[0]]
            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 명령어를 실행할 권한이 부족해 취소되었어요.\n해당 명령어를 실행하려면 미야에게 이 권한이 필요해요. `{p}`")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"<:cs_stop:665173353874587678> {ctx.author.mention} 잠시 기다려주세요. 해당 명령어를 사용하려면 {round(error.retry_after)}초를 더 기다리셔야 해요.\n해당 명령어는 `{error.cooldown.per}`초에 `{error.cooldown.rate}`번만 사용할 수 있어요.")
        elif isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            if isinstance(error, commands.MemberNotFound) or isinstance(error, commands.UserNotFound):
                await ctx.send(f":mag_right: {ctx.author.mention} `{error.argument}`(이)라는 유저를 찾을 수 없었어요. 정확한 유저를 지정해주세요!")
            elif isinstance(error, commands.ChannelNotFound):
                await ctx.send(f":mag_right: {ctx.author.mention} `{error.argument}`(이)라는 채널을 찾을 수 없었어요. 정확한 채널을 지정해주세요!")
            elif isinstance(error, commands.ChannelNotReadable):
                await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} `{error.argument}` 채널에 미야가 접근할 수 없어요. 미야가 읽을 수 있는 채널로 지정해주세요!")
            elif isinstance(error, commands.RoleNotFound):
                await ctx.send(f":mag_right: {ctx.author.mention} `{error.argument}`(이)라는 역할을 찾을 수 없었어요. 정확한 역할을 지정해주세요!")
            else:
                usage = ctx.command.help.split("\n")[0]
                await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `{usage}`(이)가 올바른 명령어에요!")
        else:
            await webhook.terminal(f"An error occurred while running command {ctx.command.name} : {error}", "미야 Terminal", self.miya.user.avatar_url)
            print(f"An error occurred while running command {ctx.command.name} : {error}")
            await ctx.send(f":warning: {ctx.author.mention} 명령어 실행 도중 오류가 발생했어요.\n이 오류가 지속될 경우 Discord 지원 서버로 문의해주세요. https://discord.gg/mdgaSjB")

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return

        if msg.channel.type == discord.ChannelType.private:
            return

        if 'discord.gg' in msg.content or 'discord.com/invite' in msg.content or 'discordapp.com/invite' in msg.content:
            result = await data.load('guilds', 'guild', msg.guild.id)
            if result is not None:
                if result[3] == 'true':
                    if msg.channel.topic is None or '=무시' not in msg.channel.topic:
                        await msg.delete()
                        await msg.channel.send(f"<:cs_trash:659355468631769101> {msg.author.mention} 서버 설정에 따라 이 채널에는 Discord 초대 링크를 포스트하실 수 없어요.")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await webhook.terminal(f"Added to {guild.name} ( {guild.id} )", "미야 Terminal", self.miya.user.avatar_url)
        print(f"Added to {guild.name} ( {guild.id} )")
        try:
            embed = discord.Embed(title="미야를 초대해주셔서 감사해요!", 
                description="""`미야야 채널설정 공지 < #채널 >` 명령어를 사용해 공지 채널을 설정해주세요.
                    미야에 관련된 문의 사항은 [지원 서버](https://discord.gg/mdgaSjB)에서 하실 수 있어요!
                    미야의 더욱 다양한 명령어는 `미야야 도움말` 명령어로 살펴보세요!
                    """, color=0x5FE9FF)
            await guild.owner.send(f"<:cs_notify:659355468904529920> {guild.owner.mention}", embed=embed)
        except:
            return
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await webhook.terminal(f"Removed from {guild.name} ( {guild.id} )", "미야 Terminal", self.miya.user.avatar_url)
        print(f"Removed from {guild.name} ( {guild.id} )")

    @commands.Cog.listener()
    async def on_member_join(self, member):
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
    miya.add_cog(Listeners(miya))
