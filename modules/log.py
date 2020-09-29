import discord
from discord.ext import commands
from utils import data
import datetime

class log(commands.Cog, name="로그"):
    def __init__(self, miya):
        self.miya = miya
    
    async def get_channel(self, guild_id):
        result = await data.load('eventLog', 'guild', guild_id)
        channel = self.miya.get_channel(int(result[1]))
        if channel is not None:
            return channel
        else:
            return None
    
    async def get_events(self, guild_id):
        result = await data.load('eventLog', 'guild', guild_id)
        events = result[2]
        if events == "None" or events == None:
            return None
        else:
            return events

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = await log.get_channel(self, member.guild.id)
        event = await log.get_events(self, member.guild.id)
        if channel is not None and event is not None:
            if "멤버 입장" not in event:
                return
            else:
                embed = discord.Embed(title="유저가 서버에 입장했습니다.", description=f"< 입장한 유저 : {member.mention}\n", timestamp=member.joined_at, color=0x15ff0e)
                embed.set_thumbnail(url=member.avatar_url_as(static_format="png", size=2048))
                embed.set_footer(text="이벤트 MEMBER_JOIN")
                await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = await log.get_channel(self, member.guild.id)
        event = await log.get_events(self, member.guild.id)
        if channel is not None and event is not None:
            if "멤버 퇴장" not in event:
                return
            else:
                roles = ""
                for role in member.roles:
                    roles += f"{role.mention} "
                embed = discord.Embed(title="유저가 서버에서 나갔습니다.", description=f"< 퇴장한 유저 : {member.mention}\n< 가지고 있던 역할 {roles}", timestamp=member.joined_at, color=0xff0000)
                embed.set_thumbnail(url=member.avatar_url_as(static_format="png", size=2048))
                embed.set_footer(text="이벤트 MEMBER_REMOVE")
                await channel.send(embed=embed)
                
    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        channel = await log.get_channel(self, payload.guild_id)
        event = await log.get_events(self, payload.guild_id)
        if channel is not None and event is not None:
            if "메시지 삭제" not in event:
                return
            else:
                if payload.cached_message is not None:
                    msg = payload.cached_message
                    embed = discord.Embed(title="메시지가 삭제되었습니다.", timestamp=datetime.datetime.now(), color=0xff0000)
                    embed.add_field(name="메시지 주인", value=f"{msg.author.mention} ( {msg.author.id} )")
                    embed.add_field(name="메시지가 삭제된 채널", value=f"{msg.channel.mention} ( {msg.channel.id} )")
                    if msg.content == "" and msg.attachments:
                        embed.add_field(name="메시지 내용", value="*내용이 없습니다. (싸늘한 바람)*")
                        embed.add_field(name="파일", value="파일이 아래 업로드되었습니다.")
                        await channel.send(embed=embed)
                        await channel.send(files=msg.attachments)
                    elif msg.content != "" and msg.attachments:
                        embed.add_field(name="메시지 내용", value=msg.content)
                        embed.add_field(name="파일", value="파일이 아래 업로드되었습니다.")
                        await channel.send(embed=embed)
                        await channel.send(files=msg.attachments)
                    else:
                        embed.add_field(name="메시지 내용", value=msg.content)
                        embed.add_field(name="파일", value="*파일이 없습니다. (싸늘한 바람)*")
                        await channel.send(embed=embed)
                else:
                    embed = discord.Embed(title="메시지가 삭제되었습니다.", description="메시지가 캐싱되지 않아 내용 및 파일을 불러오지 못했습니다.", timestamp=datetime.datetime.now())
                    embed.add_field(name="메시지가 삭제된 채널", value=f"<#{payload.channel_id}> ( {payload.channel_id} )")
                    await channel.send(embed=embed)

