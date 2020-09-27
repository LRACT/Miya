import discord
from discord.ext import commands 
from utils import data
import asyncio

class Liszt(commands.Cog, name="서버 데이터 관리"): 
    def __init__(self, miya):
        self.miya = miya
    
    @commands.command(name="등록")
    @commands.has_permissions(manage_guild=True)
    async def register(self, ctx): 
        result = await data.load('guilds', 'guild', ctx.guild.id)
        if result is None:        
            embed = discord.Embed(description="미야 이용 약관에 동의 하시겠습니까?\n \n`미야`의 서비스를 해당 서버에서 사용하실려면 약관에 동의해야 해요.\n`동의합니다`를 입력하여 이용약관에 동의하실 수 있어요!\n \n[이용 약관](https://miya.kro.kr/tos)")
            register_msg = await ctx.send(f"{ctx.author.mention}", embed=embed) 
            def check(msg): 
                return msg.channel == ctx.channel and msg.author == ctx.author and msg.content == "동의합니다"
            try: 
                await self.miya.wait_for('message', timeout=180, check=check)
            except asyncio.TimeoutError:
                fail_embed = discord.Embed(description="미야 이용약관 동의에 시간이 너무 오래 걸려 취소되었습니다.", color=0xFF0000)
                await register_msg.edit(embed=fail_embed)
            else:
                await register_msg.delete()
                uploading = await ctx.send(f"<a:cs_wait:659355470418411521> {ctx.author.mention} 잠시만 기다려주세요... DB에서 당신의 요청을 처리하고 있어요!")
                g_result = await data.insert('guilds', 'guild, muteRole', f'{ctx.guild.id}, 1234')
                e_result = await data.insert('eventLog', 'guild, channel, events', f'{ctx.guild.id}, 1234, "None"')
                default_join_msg = "{member}님 **{guild}**에 오신 것을 환영해요! 현재 인원 : {count}명"
                default_quit_msg = "{member}님 잘가세요.. 현재 인원 : {count}명"
                m_result = await data.insert('memberNoti', 'guild, channel, join_msg, remove_msg', f'{ctx.guild.id}, 1234, "{default_join_msg}", "{default_quit_msg}"')
                if g_result == "SUCCESS" and e_result == "SUCCESS" and m_result == "SUCCESS":
                    print(f"Guild registered :: {ctx.guild.name} ( {ctx.guild.id} )")
                    await uploading.edit(content=f"<:cs_yes:659355468715786262> {ctx.author.mention} 서버 등록이 완료되었어요! 이제 미야의 기능을 사용하실 수 있어요.")
                else:
                    print(f"Guild register failed :: {ctx.guild.name} ( {ctx.guild.id} )")
                    print(f"{ctx.guild.id} guild Table :: {g_result}")
                    print(f"{ctx.guild.id} memberNoti Table :: {m_result}")
                    print(f"{ctx.guild.id} eventLog Table :: {e_result}")
                    await uploading.edit(content=f"<:cs_no:659355468816187405> {ctx.author.mention} 서버 등록 도중에 오류가 발생했습니다. 등록을 다시 시도해주세요.\n계속해서 이런 현상이 발생한다면 https://discord.gg/mdgaSjB 로 문의해주세요.")
        else:
            await ctx.send(f"<:cs_id:659355469034422282> {ctx.author.mention} 서버가 이미 등록되어 있는 것으로 확인되었습니다.\n등록되지 않았는데 이 문구가 뜬다면 https://discord.gg/mdgaSjB 로 문의해주세요.")

def setup(miya):
    miya.add_cog(Liszt(miya))