import discord
from discord.ext import commands
from utils import data
import datetime
import locale
locale.setlocale(locale.LC_ALL, '')


class log(commands.Cog, name="로그"):
    def __init__(self, miya):
        self.miya = miya

    async def get_channel(self, guild_id):
        rows = await data.fetch(f"SELECT * FROM `guilds` WHERE `guild` = '{guild_id}'")
        if rows:
            channel = self.miya.get_channel(int(rows[0][1]))
            if channel is not None:
                return channel
            else:
                return None
        else:
            return None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = await log.get_channel(self, member.guild.id)
        if channel is not None:
            try:
                embed = discord.Embed(
                    title="유저가 서버에 입장했습니다.", description=f"< 입장한 유저 : {member.mention}\n", timestamp=member.joined_at, color=0x15ff0e)
                embed.set_thumbnail(url=member.avatar_url_as(
                    static_format="png", size=2048))
                embed.set_footer(text="멤버 입장 이벤트")
                embed.set_author(name="기록", icon_url=self.miya.user.avatar_url)
                await channel.send(embed=embed)
            except:
                return

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = await log.get_channel(self, member.guild.id)
        if channel is not None:
            try:
                roles = ""
                for role in member.roles:
                    roles += f"{role.mention} "
                embed = discord.Embed(
                    title="유저가 서버에서 나갔습니다.", description=f"< 퇴장한 유저 : {member.mention}\n< 가지고 있던 역할 {roles}", timestamp=member.joined_at, color=0xff0000)
                embed.set_thumbnail(url=member.avatar_url_as(
                    static_format="png", size=2048))
                embed.set_footer(text="멤버 퇴장 이벤트")
                embed.set_author(name="기록", icon_url=self.miya.user.avatar_url)
                await channel.send(embed=embed)
            except:
                return

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        channel = await log.get_channel(self, payload.guild_id)
        if channel is not None:
            try:
                if payload.cached_message is not None:
                    msg = payload.cached_message
                    if msg.author.bot:
                        return

                    embed = discord.Embed(
                        title="메시지가 삭제되었습니다.", timestamp=datetime.datetime.utcnow(), color=0xff0000)
                    embed.add_field(
                        name="메시지 주인", value=f"{msg.author.mention} ( {msg.author.id} )", inline=False)
                    embed.add_field(
                        name="메시지가 삭제된 채널", value=f"{msg.channel.mention} ( {msg.channel.id} )", inline=False)
                    embed.set_thumbnail(url=msg.author.avatar_url_as(
                        static_format="png", size=2048))
                    embed.set_footer(text="메시지 삭제 이벤트")
                    embed.set_author(
                        name="기록", icon_url=self.miya.user.avatar_url)
                    if msg.content == "":
                        embed.add_field(
                            name="메시지 내용", value="*내용이 없습니다. (싸늘한 바람)*", inline=False)
                        await channel.send(embed=embed)
                    elif msg.content != "":
                        embed.add_field(
                            name="메시지 내용", value=msg.content, inline=False)
                        await channel.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="메시지가 삭제되었습니다.", description="메시지가 캐싱되지 않아 내용 및 파일을 불러오지 못했습니다.", timestamp=datetime.datetime.utcnow())
                    embed.add_field(
                        name="메시지가 삭제된 채널", value=f"<#{payload.channel_id}> ( {payload.channel_id} )", inline=False)
                    embed.set_author(
                        name="기록", icon_url=self.miya.user.avatar_url)
                    await channel.send(embed=embed)
            except:
                return

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot and after.author.bot:
            return

        channel = await log.get_channel(self, before.guild.id)
        if channel is not None:
            try:
                embed = discord.Embed(
                    title="메시지가 수정되었습니다.", timestamp=datetime.datetime.utcnow(), color=0xff0000)
                embed.add_field(
                    name="메시지 주인", value=f"{after.author.mention} ( {after.author.id} )", inline=False)
                embed.add_field(
                    name="메시지가 수정된 채널", value=f"{after.channel.mention} ( {after.channel.id} )", inline=False)
                embed.add_field(
                    name="메시지로 이동하기", value=f"[메시지 바로가기](https://discord.com/channels/{after.guild.id}/{after.channel.id}/{after.id})", inline=False)
                embed.add_field(name="메시지 수정 전 내용",
                                value=f"내용 : {before.content}", inline=False)
                embed.add_field(name="메시지 수정 후 내용",
                                value=f"내용 : {after.content}", inline=False)
                embed.set_thumbnail(url=after.author.avatar_url_as(
                    static_format="png", size=2048))
                embed.set_footer(text="메시지 수정 이벤트")
                if before.pinned == True and after.pinned == False:
                    embed.add_field(name="변경된 사항", value="메시지 고정이 해제됨")
                elif before.pinned == False and after.pinned == True:
                    embed.add_field(name="변경된 사항", value="메시지가 고정됨")
                elif len(before.embeds) != len(after.embeds):
                    embed.add_field(name="변경된 사항", value="임베드가 변경됨")
                embed.set_author(name="기록", icon_url=self.miya.user.avatar_url)
                await channel.send(embed=embed)
            except:
                return


def setup(miya):
    miya.add_cog(log(miya))
