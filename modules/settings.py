import discord
from discord.ext import commands
from utils import data, webhook
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
        working = await ctx.send(f"<a:cs_wait:659355470418411521> {ctx.author.mention} 잠시만 기다려주세요... API와 DB에서 당신의 요청을 처리하고 있어요!")
        try:
            await ctx.guild.me.add_roles(role)
        except:
            await working.edit(content=f"<:cs_console:659355468786958356> {ctx.author.mention} 지정하려는 역할이 봇보다 높아요. 설정하려는 역할을 봇의 최상위 역할보다 낮춰주세요.")
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
                await working.edit(content=f"<:cs_settings:659355468992610304> {ctx.author.mention} `{role.name}` 역할로 뮤트를 설정했어요.\n \n*관리자 및 권한 설정을 통해 메시지 보내기 권한을 승인된 유저는 뮤트가 적용되지 않아요.*")
            else:
                await webhook.terminal(f"Channel set failed. guilds Result :: {result}", "미야 Terminal", self.miya.user.avatar_url)
                print(f"Mute role update failed. guilds Result :: {result}")
                await working.edit(content=f":warning: {ctx.author.mention} 명령어 실행 도중 오류가 발생했어요.\n이 오류가 지속될 경우 Discord 지원 서버로 문의해주세요. https://discord.gg/mdgaSjB")

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
                working = await ctx.send(f"<a:cs_wait:659355470418411521> {ctx.author.mention} 잠시만 기다려주세요... API와 DB에서 당신의 요청을 처리하고 있어요!")
                channel = ctx.message.channel_mentions[0]
                value = None
                table = None
                if args[0] == "공지":
                    follow = self.miya.get_channel(config.NotifyChannel)
                    try:
                        await follow.follow(destination=channel, reason="미야 봇 공지 채널 설정")
                    except discord.Forbidden:
                        await working.edit(content=f"<:cs_no:659355468816187405> {ctx.author.mention} 공지 채널 설정은 해당 채널에 웹훅 관리 권한이 필요해요.")
                    else:
                        await working.edit(content=f"<:cs_settings:659355468992610304> {ctx.author.mention} {channel.mention} 채널에 미야 지원 서버의 공지 채널을 팔로우했어요.\n \n*미야의 공지를 더 이상 받고 싶지 않다면 서버의 연동 설정에서 팔로우를 취소해주세요!*")
                else:
                    if args[0] == "로그":
                        table = "guilds"
                        value = "eventLog"
                    elif args[0] == "입퇴장":
                        table = "memberNoti"
                        value = "channel"
                    if value is not None and table is not None:
                        result = await data.update(table, value, channel.id, 'guild', ctx.guild.id)
                        if result == "SUCCESS":
                            await working.edit(content=f"<:cs_settings:659355468992610304> {ctx.author.mention} {args[0]} 채널을 {channel.mention} 채널로 설정했어요.")
                        else:
                            await webhook.terminal(f"Channel set failed. {table} Result :: {result}", "미야 Terminal", self.miya.user.avatar_url)
                            print(f"Channel set failed. {table} Result :: {result}")
                            await working.edit(content=f":warning: {ctx.author.mention} 명령어 실행 도중 오류가 발생했어요.\n이 오류가 지속될 경우 Discord 지원 서버로 문의해주세요. https://discord.gg/mdgaSjB")
                    else:
                        await working.edit(content=f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 채널설정 < 공지 / 로그 / 입퇴장 > < #채널 >`(이)가 올바른 명령어에요!")
    
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
                working = await ctx.send(f"<a:cs_wait:659355470418411521> {ctx.author.mention} 잠시만 기다려주세요... API와 DB에서 당신의 요청을 처리하고 있어요!")
                result = await data.update('guilds', 'linkFiltering', "true", 'guild', ctx.guild.id)
                if result == "SUCCESS":
                    await working.edit(content=f"<:cs_on:659355468682231810> {ctx.author.mention} 링크 차단 기능을 활성화했어요!")
                else:
                    await webhook.terminal(f"Filtering set failed. guilds Result :: {result}", "미야 Terminal", self.miya.user.avatar_url)
                    print(f"Filtering set failed. guilds Result :: {result}")
                    await working.edit(content=f":warning: {ctx.author.mention} 명령어 실행 도중 오류가 발생했어요.\n이 오류가 지속될 경우 Discord 지원 서버로 문의해주세요. https://discord.gg/mdgaSjB")
            elif args[0] == "끄기":
                working = await ctx.send(f"<a:cs_wait:659355470418411521> {ctx.author.mention} 잠시만 기다려주세요... API와 DB에서 당신의 요청을 처리하고 있어요!")
                result = await data.update('guilds', 'linkFiltering', "false", 'guild', ctx.guild.id)
                if result == "SUCCESS":
                    await working.edit(content=f"<:cs_off:659355468887490560> {ctx.author.mention} 링크 차단 기능을 비활성화했어요!")
                else:
                    await webhook.terminal(f"Filtering set failed. guilds Result :: {result}", "미야 Terminal", self.miya.user.avatar_url)
                    print(f"Filtering set failed. guilds Result :: {result}")
                    await working.edit(content=f":warning: {ctx.author.mention} 명령어 실행 도중 오류가 발생했어요.\n이 오류가 지속될 경우 Discord 지원 서버로 문의해주세요. https://discord.gg/mdgaSjB")
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
                    working = await ctx.send(f"<a:cs_wait:659355470418411521> {ctx.author.mention} 잠시만 기다려주세요... API와 DB에서 당신의 요청을 처리하고 있어요!")
                    msg = ""
                    for arg in local:
                        msg += f"{arg} "
                    result = await data.update("memberNoti", value, msg, 'guild', ctx.guild.id)
                    if result == "SUCCESS":
                        a = msg.replace("{member}", str(ctx.author.mention))
                        a = a.replace("{guild}", str(ctx.guild.name))
                        a = a.replace("{count}", str(ctx.guild.member_count))
                        await working.edit(content=f"<:cs_settings:659355468992610304> {ctx.author.mention} {args[0]} 메시지를 성공적으로 변경했어요!\n이제 유저가 {args[0]} 시 채널에 이렇게 표시될 거에요. : \n{a}")
                    else:
                        await webhook.terminal(f"Message set failed. Result :: {result}", "미야 Terminal", self.miya.user.avatar_url)
                        print(f"Message set failed. Result :: {result}")
                        await working.edit(content=f":warning: {ctx.author.mention} 명령어 실행 도중 오류가 발생했어요.\n이 오류가 지속될 경우 Discord 지원 서버로 문의해주세요. https://discord.gg/mdgaSjB")            
            else:
                await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 메시지설정 < 입장 / 퇴장 > < 메시지 >`(이)가 올바른 명령어에요!")

def setup(miya):
    miya.add_cog(settings(miya)) 