import discord
from discord.ext import commands
import json
import requests 
from utils import data

class handler(commands.Cog):
    def __init__(self, miya):
        self.miya = miya
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(self.miya.user)
        print(self.miya.user.id)
        await self.miya.change_presence(status=discord.Status.online, activity=discord.Game("'미야야 도움' 이라고 말해보세요!"))
        print("READY")
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            url = "https://builder.pingpong.us/api/builder/5e5b4a6ae4b0147906135955/integration/v0.2/custom/a2V5OjY2ZjhhM2Q0MmEyM2Q3NDhjZDUwNDdkMmNmMTI5ZDg1"
            headers = {
                'Authorization': 'Basic a2V5OjY2ZjhhM2Q0MmEyM2Q3NDhjZDUwNDdkMmNmMTI5ZDg1', 'Content-Type': 'application/json'
            }
            def chat(text):
                data = dict() 
                request = dict() 
                request["query"] = text
                data["request"] = request
                return requests.post(url, headers=headers, data=json.dumps(data).encode('utf-8'))

            embed = discord.Embed(title=chat(ctx.message.content.replace("미야야 ", "")).json()['response']['replies'][0]["text"], description="[지원 서버 접속하기](https://discord.gg/mdgaSjB)\n[한국 디스코드 봇 리스트 하트누르기](https://koreanbots.dev/bots/720724942873821316)")
            await ctx.send(embed = embed)
        else:
            await ctx.send(error)
            
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot == False:
            value = await data.load(member.guild.id, "memberNoti")
            if value is None:
                return
            else:
                channel = member.guild.get_channel(int(value[1]))
                if channel is not None and value[2] != "":
                    msg = value[2].replace("{member}", str(member))
                    msg = msg.replace("{guild}", str(member.guild.name))
                    msg = msg.replace("{count}", str(member.guild.member_count))
                    await channel.send(msg)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.bot == False:
            value = await data.load(member.guild.id, "memberNoti")
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
    miya.add_cog(handler(miya))