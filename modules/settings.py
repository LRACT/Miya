import discord
from discord.ext import commands
from utils import data, webhook
from lib import config
import locale

locale.setlocale(locale.LC_ALL, "")


class Settings(commands.Cog, name="설정"):
    def __init__(self, miya):
        self.miya = miya

    @commands.command(name="뮤트설정")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(
        manage_channels=True, manage_roles=True, manage_permissions=True
    )
    async def role_set(self, ctx, role: discord.Role):
        """
        미야야 뮤트설정 < @역할 >


        미야의 뮤트 명령어를 사용 시 적용할 역할을 설정합니다.
        """
        if role >= ctx.guild.me.top_role:
            await ctx.send(
                f"<:cs_console:659355468786958356> {ctx.author.mention} 지정하려는 역할이 봇보다 높거나 같아요. 설정하려는 역할을 봇의 최상위 역할보다 낮춰주세요."
            )
        else:
            async with ctx.channel.typing():
                result = await data.commit(
                    f"UPDATE `guilds` SET `muteRole` = '{role.id}' WHERE `guild` = '{ctx.guild.id}'"
                )
                if result == "SUCCESS":
                    for channel in ctx.guild.text_channels:
                        perms = channel.overwrites_for(role)
                        perms.send_messages = False
                        perms.send_tts_messages = False
                        perms.add_reactions = False
                        await channel.set_permissions(
                            role, overwrite=perms, reason="뮤트 역할 설정"
                        )
                    for channel in ctx.guild.voice_channels:
                        perms = channel.overwrites_for(role)
                        perms.speak = False
                        perms.stream = False
                        await channel.set_permissions(
                            role, overwrite=perms, reason="뮤트 역할 설정"
                        )
                    for category in ctx.guild.categories:
                        perms = category.overwrites_for(role)
                        perms.send_messages = False
                        perms.send_tts_messages = False
                        perms.add_reactions = False
                        perms.speak = False
                        perms.stream = False
                        await category.set_permissions(
                            role, overwrite=perms, reason="뮤트 역할 설정"
                        )
                    await ctx.reply(
                        f"<:cs_settings:659355468992610304> 뮤트 역할을 `{role.name}` 역할로 설정했어요.\n \n*관리자 권한을 가진 유저 및 권한 설정을 통해 메시지 보내기 권한을 승인받은 유저는 뮤트가 적용되지 않아요.*"
                    )
                else:
                    await webhook.terminal(
                        f"Mute Update Failed >\nSQL Result - {result}",
                        "명령어 처리 기록",
                        self.miya.user.avatar_url,
                    )
                    await ctx.reply(
                        f":warning: 명령어 실행 도중 오류가 발생했어요.\n오류 해결을 위해 Discord 지원 서버로 문의해주세요. https://discord.gg/tu4NKbEEnn"
                    )

    @commands.command(name="채널설정")
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_webhooks=True)
    async def ch_set(self, ctx, what, channel: discord.TextChannel):
        """
        미야야 채널설정 < 공지 / 로그 / 입퇴장 > < #채널 >


        미야의 공지사항, 입퇴장 메세지를 전송할 채널, 각종 로그를 전송할 채널을 설정합니다.
        """
        value = None
        table = None
        async with ctx.channel.typing():
            if what == "공지":
                if channel.type == discord.ChannelType.news:
                    await ctx.reply(
                        f"<:cs_no:659355468816187405> 미야 공지 채널은 Discord 커뮤니티 공지 채널이 아닌 곳에만 설정할 수 있어요."
                    )
                else:
                    follow = self.miya.get_channel(config.NotifyChannel)
                    try:
                        await follow.follow(destination=channel, reason="미야 봇 공지 채널 설정")
                    except discord.Forbidden:
                        await ctx.reply(
                            f"<:cs_no:659355468816187405> 공지 채널 설정은 해당 채널에 웹훅 관리 권한이 필요해요."
                        )
                    else:
                        await ctx.reply(
                            f"<:cs_settings:659355468992610304> {channel.mention} 채널에 미야 지원 서버의 공지 채널을 팔로우했어요.\n \n*미야의 공지를 더 이상 받고 싶지 않다면 서버의 연동 설정에서 팔로우를 취소해주세요!*"
                        )
            else:
                if what == "로그":
                    table = "guilds"
                    value = "eventLog"
                elif what == "입퇴장":
                    table = "memberNoti"
                    value = "channel"
                if value is not None and table is not None:
                    result = await data.commit(
                        f"UPDATE `{table}` SET `{value}` = '{channel.id}' WHERE `guild` = '{ctx.guild.id}'"
                    )
                    if result == "SUCCESS":
                        await ctx.reply(
                            f"<:cs_settings:659355468992610304> {what} 채널을 {channel.mention} 채널로 설정했어요."
                        )
                    else:
                        await webhook.terminal(
                            f"Channel Update Failed >\nSQL Result - {result}",
                            "명령어 처리 기록",
                            self.miya.user.avatar_url,
                        )
                        await ctx.reply(
                            f":warning: 명령어 실행 도중 오류가 발생했어요.\n오류 해결을 위해 Discord 지원 서버로 문의해주세요. https://discord.gg/tu4NKbEEnn"
                        )
                else:
                    raise commands.BadArgument

    @commands.command(name="링크차단")
    @commands.has_permissions(manage_guild=True)
    async def link_set(self, ctx, *args):
        """
        미야야 링크차단 < 켜기 / 끄기 >


        서버 내에서 Discord 초대 링크를 승인할 지 삭제할 지 설정합니다.
        *채널 주제에 `=무시`라는 단어를 넣어 해당 채널만 무시할 수 있습니다.*
        """
        if not args:
            raise commands.BadArgument
        else:
            async with ctx.channel.typing():
                if args[0] == "켜기":
                    result = await data.commit(
                        f"UPDATE `guilds` SET `linkFiltering` = 'true' WHERE `guild` = '{ctx.guild.id}'"
                    )
                    if result == "SUCCESS":
                        await ctx.reply(
                            f"<:cs_on:659355468682231810> 링크 차단 기능을 활성화했어요!\n특정 채널에서만 이 기능을 끄고 싶으시다면 채널 주제에 `=무시`라는 단어를 넣어주세요."
                        )
                    else:
                        await webhook.terminal(
                            f"Filter Update Failed >\nSQL Result - {result}",
                            "명령어 처리 기록",
                            self.miya.user.avatar_url,
                        )
                        await ctx.reply(
                            f":warning: 명령어 실행 도중 오류가 발생했어요.\n오류 해결을 위해 Discord 지원 서버로 문의해주세요. https://discord.gg/tu4NKbEEnn"
                        )
                elif args[0] == "끄기":
                    result = await data.commit(
                        f"UPDATE `guilds` SET `linkFiltering` = 'false' WHERE `guild` = '{ctx.guild.id}'"
                    )
                    if result == "SUCCESS":
                        await ctx.reply(
                            f"<:cs_off:659355468887490560> 링크 차단 기능을 비활성화했어요!"
                        )
                    else:
                        await webhook.terminal(
                            f"Filter Update Failed >\nSQL Result - {result}",
                            "명령어 처리 기록",
                            self.miya.user.avatar_url,
                        )
                        await ctx.reply(
                            f":warning: 명령어 실행 도중 오류가 발생했어요.\n오류 해결을 위해 Discord 지원 서버로 문의해주세요. https://discord.gg/tu4NKbEEnn"
                        )
                else:
                    raise commands.BadArgument

    @commands.command(name="메시지설정", aliases=["메세지설정"])
    @commands.has_permissions(manage_guild=True)
    async def msg_set(self, ctx, name, *, message):
        """
        미야야 메시지설정 < 입장 / 퇴장 > < 메시지 >


        서버에 유저가 입장 혹은 퇴장할 때 전송할 메시지를 설정합니다.
        메시지 중 {member}, {guild}, {count}를 추가하여
        멘션, 서버이름, 현재인원을 메세지에 출력할 수 있습니다.
        """
        value = None
        async with ctx.channel.typing():
            if name == "입장":
                value = "join_msg"
            elif name == "퇴장":
                value = "remove_msg"
            if value is not None:
                result = await data.commit(
                    f"UPDATE `membernoti` SET `{value}` = '{message}' WHERE `guild` = '{ctx.guild.id}'"
                )
                if result == "SUCCESS":
                    a = message.replace("{member}", str(ctx.author.mention))
                    a = a.replace("{guild}", str(ctx.guild.name))
                    a = a.replace("{count}", str(ctx.guild.member_count))
                    await ctx.reply(
                        f"<:cs_settings:659355468992610304> {name} 메시지를 성공적으로 변경했어요!\n이제 유저가 {name} 시 채널에 이렇게 표시될 거에요. : \n{a}"
                    )
                else:
                    await webhook.terminal(
                        f"Message Update Failed >\nSQL Result - {result}",
                        "명령어 처리 기록",
                        self.miya.user.avatar_url,
                    )
                    await ctx.reply(
                        f":warning: 명령어 실행 도중 오류가 발생했어요.\n오류 해결을 위해 Discord 지원 서버로 문의해주세요. https://discord.gg/tu4NKbEEnn"
                    )
            else:
                raise commands.BadArgument


def setup(miya):
    miya.add_cog(Settings(miya))
