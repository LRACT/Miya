import discord
from discord.ext import commands
import json
import aiohttp
import asyncio
from utils import data, webhook
from lib import config
import datetime
import locale
locale.setlocale(locale.LC_ALL, '')

class Listeners(commands.Cog, name="이벤트 리스너"):
    def __init__(self, miya):
        self.miya = miya

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.miya.user)
        print(self.miya.user.id)        
        print("READY")
        await webhook.terminal(f"{self.miya.user}\n{self.miya.user.id}\n봇이 준비되었습니다.", "미야 Terminal", self.miya.user.avatar_url)
        uptime_set = await data.commit(f"UPDATE `miya` SET `uptime` = '{datetime.datetime.utcnow()}' WHERE `botId` = '{self.miya.user.id}'")
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
            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 권한 부족 등의 이유로 명령어 실행에 실패했어요.")
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
            if msg != "앗, 저 이번 달에 할 수 있는 말을 다 해버렸어요 🤐 다음 달까지 기다려주실거죠? ☹️":
                await webhook.terminal(f"Sent {query} to Ping Pong builder and got {msg}", "미야 Terminal", self.miya.user.avatar_url)
                print(f"Sent {query} to Ping Pong builder and got {msg}")
                embed = discord.Embed(title=msg, description=f"[Discord 지원 서버 접속하기](https://discord.gg/mdgaSjB)\n[한국 디스코드 봇 리스트 하트 누르기](https://koreanbots.dev/bots/720724942873821316)", color=0x5FE9FF)
                embed.set_footer(text="미야의 대화 기능은 https://pingpong.us/ 를 통해 제작되었습니다.")
                await ctx.send(ctx.author.mention, embed=embed)
            else:
                embed = discord.Embed(title="💭 이런, 미야가 말풍선을 모두 사용한 모양이네요.", description=f"매월 1일에 말풍선이 다시 생기니 그 때까지만 기다려주세요!\n \n[Discord 지원 서버 접속하기](https://discord.gg/mdgaSjB)\n[한국 디스코드 봇 리스트 하트 누르기](https://koreanbots.dev/bots/720724942873821316)", color=0x5FE9FF)
                embed.set_footer(text="미야의 대화 기능은 https://pingpong.us/ 를 통해 제작되었습니다.")
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
            rows = await data.fetch(f"SELECT * FROM `guilds` WHERE `guild` = '{msg.guild.id}'")
            if rows:
                if rows[0][3] == 'true':
                    if msg.channel.topic is None or '=무시' not in msg.channel.topic:
                        await msg.delete()
                        await msg.channel.send(f"<:cs_trash:659355468631769101> {msg.author.mention} 서버 설정에 따라 이 채널에는 Discord 초대 링크를 포스트하실 수 없어요.")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await webhook.terminal(f"Added to {guild.name} ( {guild.id} )", "미야 Terminal", self.miya.user.avatar_url)
        print(f"Added to {guild.name} ( {guild.id} )")
        rows = await data.fetch(f"SELECT * FROM `blacklist` WHERE `id` = '{guild.id}'")
        if rows:
            try:
                embed = discord.Embed(title="미야를 초대해주셔서 감사해요!", 
                    description="""`미야야 채널설정 공지 < #채널 >` 명령어를 사용해 공지 채널을 설정해주세요.
                        미야에 관련된 문의 사항은 [지원 서버](https://discord.gg/mdgaSjB)에서 하실 수 있어요!
                        미야의 더욱 다양한 명령어는 `미야야 도움말` 명령어로 살펴보세요!
                        """, color=0x5FE9FF)
                await guild.owner.send(f"<:cs_notify:659355468904529920> {guild.owner.mention}", embed=embed)
            except:
                await webhook.terminal(f"Couldn't send DM to server owner. : {guild.name} ( {guild.id} )", "미야 Terminal", self.miya.user.avatar_url)
                print(f"Couldn't send DM to server owner. : {guild.name} ( {guild.id} )")
        else:
            try:
                admin = self.miya.get_user(int(rows[0][1]))
                embed = discord.Embed(title="이런, 이 서버는 미야 초대가 제한되었어요!", description=f"제한에 관한 내용은 [지원 서버](https://discord.gg/mdgaSjB)로 문의해주세요.\n사유 : {rows[0][2]}\n처리한 관리자 : {admin}\n차단된 시각 : {rows[0][3]}", color=0xFF0000)
                await guild.owner.send(f"<:cs_notify:659355468904529920> {guild.owner.mention} https://discord.gg/mdgaSjB", embed=embed)
            except:
                await webhook.terminal(f"Couldn't send DM to server owner. : {guild.name} ( {guild.id} )", "미야 Terminal", self.miya.user.avatar_url)
                print(f"Couldn't send DM to server owner. : {guild.name} ( {guild.id} )")
            await webhook.terminal(f"Blacklisted guild : {guild.name} ( {guild.id} )", "미야 Terminal", self.miya.user.avatar_url)
            print(f"Blacklisted guild : {guild.name} ( {guild.id} )")
            await guild.leave()
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await webhook.terminal(f"Removed from {guild.name} ( {guild.id} )", "미야 Terminal", self.miya.user.avatar_url)
        print(f"Removed from {guild.name} ( {guild.id} )")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot == False:
            rows = await data.fetch(f"SELECT * FROM `membernoti` WHERE `guild` = '{member.guild.id}'")
            if not rows:
                return
            else:
                value = rows[0]
                channel = member.guild.get_channel(int(value[1]))
                if channel is not None and value[2] != "":
                    try:
                        msg = value[2].replace("{member}", str(member.mention))
                        msg = msg.replace("{guild}", str(member.guild.name))
                        msg = msg.replace("{count}", str(member.guild.member_count))
                        await channel.send(msg)
                    except Exception as e:
                        print(f"Can't welcome user : {member.guild} ( {member.guild.id} )\n{e}")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.bot == False:
            rows = await data.fetch(f"SELECT * FROM `membernoti` WHERE `guild` = '{member.guild.id}'")
            if not rows:
                return
            else:
                value = rows[0]
                channel = member.guild.get_channel(int(value[1]))
                if channel is not None and value[3] != "":
                    try:
                        msg = value[3].replace("{member}", str(member))
                        msg = msg.replace("{guild}", str(member.guild.name))
                        msg = msg.replace("{count}", str(member.guild.member_count))
                        await channel.send(msg)
                    except Exception as e:
                        print(f"Can't welcome user : {member.guild} ( {member.guild.id} )\n{e}")

                    
def setup(miya):
    miya.add_cog(Listeners(miya))
