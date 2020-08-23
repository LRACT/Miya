import discord
from discord.ext import commands

class handler(commands.Cog):
    def __init__(self, miya):
        self.miya = miya
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(self.miya.user)
        print(self.miya.user.id)
        await self.miya.change_presence(status=discord.Status.online, activity=discord.Game("'미야야 도움' 이라고 말해보세요!"))
        print("READY")
    
#    @commands.Cog.listener()
#    async def on_member_join(self, member):
#        # 여기에 이제 뭐 유저 알림 기능 넣어야 되고
    
#    @commands.Cog.listener()
#    async def on_member_remove(self, member):
#        # 여기에도 넣어야 되고