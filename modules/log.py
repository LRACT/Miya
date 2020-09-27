import discord
from discord.ext import commands
from utils import data

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
            if "MEMBER_JOIN" not in event:
                return
            else:
                embed = discord.Embed(title="유저가 서버에 입장했습니다.", description=f"< 입장한 유저 : {member.mention}\n", timestamp=member.joined_at)
                embed.set_thumbnail(url=member.avatar_url_as(static_format="png", size=2048))
                embed.set_footer(text="이벤트 MEMBER_JOIN")
                await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = await log.get_channel(self, member.guild.id)
        event = await log.get_events(self, member.guild.id)
        if channel is not None and event is not None:
            if "MEMBER_REMOVE" not in event:
                return
            else:
                roles = ""
                for role in member.roles:
                    roles += f"{role.mention} "
                embed = discord.Embed(title="유저가 서버에서 나갔습니다.", description=f"< 퇴장한 유저 : {member.mention}\n< 가지고 있던 역할 {roles}", timestamp=member.joined_at)
                embed.set_thumbnail(url=member.avatar_url_as(static_format="png", size=2048))
                embed.set_footer(text="이벤트 MEMBER_REMOVE")
                await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_guild_update(self, guild):
        print("Guild Updated")
