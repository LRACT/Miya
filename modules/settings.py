import discord
from discord.ext import commands
from utils import data

class settings(commands.Cog):
    def __init__(self, miya):
        self.miya = miya
    
    @commands.command(name="채널설정")
    async def ch_set(self, ctx, *args):
        """
        미야야 채널설정 < 공지 / 로그 / 입퇴장 > < #채널 >


        미야의 공지사항, 입퇴장 메세지를 전송할 채널, 각종 로그를 전송할 채널을 설정합니다.
        """
        if not args:
            await ctx.send(f"{ctx.author.mention} `미야야 채널설정 < 공지 / 로그 / 입퇴장 > < #채널 >` 이 올바른 명령어 입니다.")
        else:
            value = None
            table = None
            if args[0] == "공지":
                table = "guilds"
                value = 'announce'
            elif args[0] == "로그":
                table = "logger"
                value = "channel"
            elif args[0] == "입퇴장":
                table = "memberNoti"
                value = "channel"
            if value is not None and table is not None:
                if not ctx.message.channel_mentions: 
                    await ctx.send(f"{ctx.author.mention} `미야야 채널설정 < 공지 / 로그 / 입퇴장 > < #채널 >` 이 올바른 명령어 입니다.")
                else:
                    channel = ctx.message.channel_mentions[0]
                    result = await data.update(table, value, channel.id 'guild', ctx.guild.id)
                    if result == "SUCCESS":
                        await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
                    else:
                        await ctx.send(result)
            else:
                await ctx.send(f"{ctx.author.mention} `미야야 채널설정 < 공지 / 로그 / 입퇴장 > < #채널 >` 이 올바른 명령어 입니다.")
    
    @commands.command(name="메시지설정")
    async def msg_set(self, ctx, *args):
        """
        미야야 메시지설정 < 입장 / 퇴장 > < 메시지 >


        서버에 유저가 입장 혹은 퇴장할 때 전송할 메시지를 설정합니다.
        메시지 중 {member}, {guild}, {count}를 추가하여 
        멘션, 서버이름, 현재인원을 메세지에 출력할 수 있습니다.
        """
        if not args:
            await ctx.send(f"{ctx.author.mention} `미야야 메시지설정 < 입장 / 퇴장 > < 메시지 >` 가 올바른 명령어 입니다.")
        else:
            value = None
            if args[0] == "입장":
                value = 'join_msg'
            elif args[0] == "퇴장":
                value = 'remove_msg'
            if value is not None:
                local = args[1:]
                if not local:
                    await ctx.send(f"{ctx.author.mention} `미야야 메시지설정 < 입장 / 퇴장 > < 메시지 >` 가 올바른 명령어 입니다.")
                else:
                    msg = "".join(local)
                    result = await data.update("memberNoti", value, local, 'guild', ctx.guild.id)
                    if result == "SUCCESS":
                        await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
                    else:
                        await ctx.send(result)
            else:
                await ctx.send(f"{ctx.author.mention} `미야야 메시지설정 < 입장 / 퇴장 > < 메시지 >` 가 올바른 명령어 입니다.")

def setup(miya):
    miya.add_cog(settings(miya)) 