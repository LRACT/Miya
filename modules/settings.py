import discord
from discord.ext import commands
from utils import data, hook
from lib import config

class settings(commands.Cog, name="설정"):
    def __init__(self, miya):
        self.miya = miya

    @commands.command(name="채널설정")
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_webhooks=True)
    async def ch_set(self, ctx, *args):
        """
        미야야 채널설정 < 공지 / 로그 / 입퇴장 > < #채널 >


        미야의 공지사항, 입퇴장 메세지를 전송할 채널, 각종 로그를 전송할 채널을 설정합니다.
        """
        if not args:
            await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 채널설정 < 공지 / 로그 / 입퇴장 > < #채널 >` 이 올바른 명령어에요!")
        else:
            if not ctx.message.channel_mentions:
                await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 채널설정 < 공지 / 로그 / 입퇴장 > < #채널 >` 이 올바른 명령어에요!")
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
                            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 설정 변경 도중에 오류가 발생했습니다.\n계속해서 이런 현상이 발생한다면 https://discord.gg/mdgaSjB 로 문의해주세요.")
                    else:
                        await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 채널설정 < 공지 / 로그 / 입퇴장 > < #채널 >` 이 올바른 명령어에요!")
    
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
            await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 메시지설정 < 입장 / 퇴장 > < 메시지 >` 가 올바른 명령어에요!")
        else:
            value = None
            if args[0] == "입장":
                value = 'join_msg'
            elif args[0] == "퇴장":
                value = 'remove_msg'
            if value is not None:
                local = args[1:]
                if not local:
                    await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 메시지설정 < 입장 / 퇴장 > < 메시지 >` 가 올바른 명령어에요!")
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
                        await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 설정 변경 도중에 오류가 발생했습니다.\n계속해서 이런 현상이 발생한다면 https://discord.gg/mdgaSjB 로 문의해주세요.")
            else:
                await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 메시지설정 < 입장 / 퇴장 > < 메시지 >` 가 올바른 명령어에요!")
    
    @commands.command(name="이벤트설정")
    @commands.is_owner()
    @commands.has_permissions(manage_guild=True)
    async def event_set(self, ctx, *args):
        """
        미야야 이벤트설정 < 이벤트 이름 > < 켜기 / 끄기 >


        미야가 로깅할 이벤트를 설정합니다. `목록` 을 입력해 전체 이벤트 목록을 볼 수 있습니다.
        """
        if not args:
            await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 이벤트설정 < 이벤트 이름 > < 켜기 / 끄기 >` 가 올바른 명령어에요!\n`미야야 이벤트설정 목록`을 사용해 전체 이벤트 목록을 볼 수 있어요.")
        else:
            if args[0] == "목록":
                await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} 현재 사용 가능한 이벤트 목록\n```MEMBER_JOIN, MEMBER_REMOVE```")
                
def setup(miya):
    miya.add_cog(settings(miya)) 