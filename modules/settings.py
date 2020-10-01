import discord
from discord.ext import commands
from utils import data, hook
from lib import config

class settings(commands.Cog, name="설정"):
    def __init__(self, miya):
        self.miya = miya

    @commands.command(name="역할설정")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_channels=True, manage_roles=True, manage_permissions=True)
    async def role_set(self, ctx, role: discord.Role):
        """
        미야야 역할설정 < @역할 >


        미야의 뮤트 명령어를 사용 시 적용할 역할을 설정합니다.
        """
        try:
            await ctx.guild.me.add_roles(role)
        except:
            await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} 지정하려는 역할이 봇보다 높아요. 역할을 봇의 최상위 역할보다 낮춰주세요.")
        else:
            await ctx.guild.me.remove_roles(role)
            result = await data.update('guilds', 'muteRole', role.id, 'guild', ctx.guild.id)
            if result == "SUCCESS":
                for channel in ctx.guild.text_channels:
                    perms = channel.overwrites_for(role)
                    perms.send_messages = False
                    perms.send_tts_messages = False
                    perms.add_reactions = False
                    await channel.set_permissions(role, overwrite=perms, reason="뮤트 역할 설정")
                for channel in ctx.guild.voice_channels:
                    perms = channel.overwrites_for(role)
                    perms.speak = False
                    perms.stream = False
                    await channel.set_permissions(role, overwrite=perms, reason="뮤트 역할 설정")
                for category in ctx.guild.categories:
                    perms = category.overwrites_for(role)
                    perms.send_messages = False
                    perms.send_tts_messages = False
                    perms.add_reactions = False
                    perms.speak = False
                    perms.stream = False
                    await category.set_permissions(role, overwrite=perms, reason="뮤트 역할 설정")
                await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
            else:
                await hook.send(f"Channel set failed. guilds Result :: {result}", "미야 Terminal", self.miya.user.avatar_url)
                print(f"Mute role update failed. guilds Result :: {result}")
                await ctx.send(f":warning: {ctx.author.mention} 오류 발생; 이 오류가 지속될 경우 Discord 지원 서버로 문의해주세요. https://discord.gg/mdgaSjB")

    @commands.command(name="채널설정")
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_webhooks=True)
    async def ch_set(self, ctx, *args):
        """
        미야야 채널설정 < 공지 / 로그 / 입퇴장 > < #채널 >


        미야의 공지사항, 입퇴장 메세지를 전송할 채널, 각종 로그를 전송할 채널을 설정합니다.
        """
        if not args:
            await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 채널설정 < 공지 / 로그 / 입퇴장 > < #채널 >`(이)가 올바른 명령어에요!")
        else:
            if not ctx.message.channel_mentions:
                await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 채널설정 < 공지 / 로그 / 입퇴장 > < #채널 >`(이)가 올바른 명령어에요!")
            else:
                channel = ctx.message.channel_mentions[0]
                value = None
                table = None
                if args[0] == "공지":
                    follow = self.miya.get_channel(config.NotifyChannel)
                    try:
                        await follow.follow(destination=channel, reason="미야 봇 공지 채널 설정")
                    except discord.Forbidden:
                        await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 공지 채널 설정은 해당 채널에 웹훅 관리 권한이 필요해요.")
                    else:
                        await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
                else:
                    if args[0] == "로그":
                        table = "eventLog"
                        value = "channel"
                    elif args[0] == "입퇴장":
                        table = "memberNoti"
                        value = "channel"
                    if value is not None and table is not None and args[0] != "공지":
                        result = await data.update(table, value, channel.id, 'guild', ctx.guild.id)
                        if result == "SUCCESS":
                            await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
                        else:
                            await hook.send(f"Channel set failed. {table} Result :: {result}", "미야 Terminal", self.miya.user.avatar_url)
                            print(f"Channel set failed. {table} Result :: {result}")
                            await ctx.send(f":warning: {ctx.author.mention} 오류 발생; 이 오류가 지속될 경우 Discord 지원 서버로 문의해주세요. https://discord.gg/mdgaSjB")
                    else:
                        await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 채널설정 < 공지 / 로그 / 입퇴장 > < #채널 >`(이)가 올바른 명령어에요!")
    
    @commands.command(name="링크차단")
    @commands.has_permissions(manage_guild=True)
    async def link_set(self, ctx, *args):
        """
        미야야 링크차단 < 켜기 / 끄기 >


        서버 내에서 Discord 초대 링크를 승인할 지 삭제할 지 설정합니다.
        *채널 주제에 `=무시`라는 단어를 넣어 해당 채널만 무시할 수 있습니다.*
        """
        if not args:
            await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 링크차단 < 켜기 / 끄기 >`(이)가 올바른 명령어에요!")
        else:
            if args[0] == "켜기":
                result = await data.update('guilds', 'linkFiltering', "true", 'guild', ctx.guild.id)
                if result == "SUCCESS":
                    await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
                else:
                    await hook.send(f"Filtering set failed. guilds Result :: {result}", "미야 Terminal", self.miya.user.avatar_url)
                    print(f"Filtering set failed. guilds Result :: {result}")
                    await ctx.send(f":warning: {ctx.author.mention} 오류 발생; 이 오류가 지속될 경우 Discord 지원 서버로 문의해주세요. https://discord.gg/mdgaSjB")
            elif args[0] == "끄기":
                result = await data.update('guilds', 'linkFiltering', "false", 'guild', ctx.guild.id)
                if result == "SUCCESS":
                    await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
                else:
                    await hook.send(f"Filtering set failed. guilds Result :: {result}", "미야 Terminal", self.miya.user.avatar_url)
                    print(f"Filtering set failed. guilds Result :: {result}")
                    await ctx.send(f":warning: {ctx.author.mention} 오류 발생; 이 오류가 지속될 경우 Discord 지원 서버로 문의해주세요. https://discord.gg/mdgaSjB")
            else:
                await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 링크차단 < 켜기 / 끄기 >`(이)가 올바른 명령어에요!")
            
    
    @commands.command(name="메시지설정")
    @commands.has_permissions(manage_guild=True)
    async def msg_set(self, ctx, *args):
        """
        미야야 메시지설정 < 입장 / 퇴장 > < 메시지 >


        서버에 유저가 입장 혹은 퇴장할 때 전송할 메시지를 설정합니다.
        메시지 중 {member}, {guild}, {count}를 추가하여 
        멘션, 서버이름, 현재인원을 메세지에 출력할 수 있습니다.
        """
        if not args:
            await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 메시지설정 < 입장 / 퇴장 > < 메시지 >`(이)가 올바른 명령어에요!")
        else:
            value = None
            if args[0] == "입장":
                value = 'join_msg'
            elif args[0] == "퇴장":
                value = 'remove_msg'
            if value is not None:
                local = args[1:]
                if not local:
                    await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 메시지설정 < 입장 / 퇴장 > < 메시지 >`(이)가 올바른 명령어에요!")
                else:
                    msg = ""
                    for arg in local:
                        msg += f"{arg} "
                    result = await data.update("memberNoti", value, msg, 'guild', ctx.guild.id)
                    if result == "SUCCESS":
                        await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
                    else:
                        await hook.send(f"Message set failed. Result :: {result}", "미야 Terminal", self.miya.user.avatar_url)
                        print(f"Message set failed. Result :: {result}")
                        await ctx.send(f":warning: {ctx.author.mention} 오류 발생; 이 오류가 지속될 경우 Discord 지원 서버로 문의해주세요. https://discord.gg/mdgaSjB")
            else:
                await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 메시지설정 < 입장 / 퇴장 > < 메시지 >`(이)가 올바른 명령어에요!")
    
    @commands.command(name="이벤트설정")
    @commands.is_owner()
    @commands.has_permissions(manage_guild=True)
    async def event_set(self, ctx, *args):
        """
        미야야 이벤트설정 < 이벤트 이름 > < 켜기 / 끄기 >


        미야가 로깅할 이벤트를 설정합니다. `목록` 을 입력해 전체 이벤트 목록을 볼 수 있습니다.
        """
        if not args:
            await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 이벤트설정 < 목록 / 이벤트 이름 > [ 켜기 / 끄기 ]`(이)가 올바른 명령어에요!\n`미야야 이벤트설정 목록`을 사용해 전체 이벤트 목록을 볼 수 있어요.")
        else:
            if args[0] == "목록":
                await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} 현재 사용 가능한 이벤트 목록\n```멤버 입장, 멤버 퇴장, 메시지 삭제, 메시지 수정```")
            else:
                enable = None
                if args[2] == "켜기":
                    enable = True
                if args[2] == "끄기":
                    enable = False
                if enable is not None:
                    if args[0] == "멤버":
                        if args[1] == "입장":
                            result = await data.load('eventLog', 'guild', ctx.guild.id)
                            if enable == True:
                                if "멤버 입장" in result[2]:
                                    await data.update() 

def setup(miya):
    miya.add_cog(settings(miya)) 