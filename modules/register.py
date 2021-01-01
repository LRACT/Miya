import discord
from discord.ext import commands 
from utils import data, webhook
import asyncio
import locale
locale.setlocale(locale.LC_ALL, '')

class DataManagement(commands.Cog, name="서버 데이터 관리"): 
    def __init__(self, miya):
        self.miya = miya
    
    @commands.command(name="등록")
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def register(self, ctx):
        """
        미야야 등록


        미야 DB에 서버를 등록합니다. *이용 약관에 동의해야 합니다.*
        """
        result = await data.load('guilds', 'guild', ctx.guild.id)
        if result is None:        
            embed = discord.Embed(title="미야 이용 약관에 동의하시겠어요?", description="`미야`의 서비스를 해당 서버에서 사용하시려면 약관에 동의해야 해요.\n`동의합니다`를 입력하여 이용 약관에 동의하실 수 있어요!\n \n[이용 약관](https://miya.kro.kr/tos)\n[개인정보보호방침](https://miya.kro.kr/privacy)", color=0x5FE9FF)
            register_msg = await ctx.send(f"{ctx.author.mention}", embed=embed) 
            def check(msg): 
                return msg.channel == ctx.channel and msg.author == ctx.author and msg.content == "동의합니다"
            try: 
                msg = await self.miya.wait_for('message', timeout=180, check=check)
            except asyncio.TimeoutError:
                fail_embed = discord.Embed(description="미야 이용약관 동의에 시간이 너무 오래 걸려 취소되었습니다.", color=0xFF0000)
                await register_msg.edit(embed=fail_embed)
            else:
                await msg.delete()
                await register_msg.delete()
                working = await ctx.send(f"<a:cs_wait:659355470418411521> {ctx.author.mention} 잠시만 기다려주세요... DB에서 당신의 요청을 처리하고 있어요!")
                g_result = await data.insert('guilds', '`guild`, `eventLog`, `muteRole`, `linkFiltering`, `warn_kick`', f'"{ctx.guild.id}", "1234", "1234", "false", "0"')
                default_join_msg = "{member}님 **{guild}**에 오신 것을 환영해요! 현재 인원 : {count}명"
                default_quit_msg = "{member}님 안녕히 가세요.. 현재 인원 : {count}명"
                m_result = await data.insert('memberNoti', '`guild`, `channel`, `join_msg`, `remove_msg`', f'"{ctx.guild.id}", "1234", "{default_join_msg}", "{default_quit_msg}"')
                if g_result == "SUCCESS" and m_result == "SUCCESS":
                    await webhook.terminal(f"Guild registered :: {ctx.guild.name} ( {ctx.guild.id} )", "미야 Terminal", self.miya.user.avatar_url)
                    print(f"Guild registered :: {ctx.guild.name} ( {ctx.guild.id} )")
                    await working.edit(content=f"<:cs_yes:659355468715786262> {ctx.author.mention} 서버 등록이 완료되었어요! 이제 미야의 기능을 사용하실 수 있어요.")
                else:
                    await webhook.terminal(f"Guild register failed :: {ctx.guild.name} ( {ctx.guild.id} )\n{ctx.guild.id} guild Table :: {g_result}\n{ctx.guild.id} memberNoti Table :: {m_result}", "미야 Terminal", self.miya.user.avatar_url)
                    print(f"Guild register failed :: {ctx.guild.name} ( {ctx.guild.id} )\n{ctx.guild.id} guild Table :: {g_result}\n{ctx.guild.id} memberNoti Table :: {m_result}")
                    await working.edit(content=f"<:cs_no:659355468816187405> {ctx.author.mention} 서버 등록 도중에 오류가 발생했어요. 등록을 다시 시도해주세요.\n계속해서 이런 현상이 발생한다면 https://discord.gg/mdgaSjB 로 문의해주세요.")
        else:
            await ctx.send(f"<:cs_id:659355469034422282> {ctx.author.mention} 서버가 이미 등록되어 있는 것 같아요.\n등록되지 않았는데 이 문구가 뜬다면 https://discord.gg/mdgaSjB 로 문의해주세요.")

def setup(miya):
    miya.add_cog(DataManagement(miya))