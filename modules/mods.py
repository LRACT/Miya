import discord
from discord.ext import commands
import asyncio
import typing
from utils import data

class Moderation(commands.Cog, name="관리"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="뮤트")
    @commands.has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    async def _mute(self, ctx, member: discord.Member):
        result = await data.load('guilds', 'guild', ctx.guild.id)
        role = ctx.guild.get_role(int(result[1]))
        if role is not None:
            await member.add_roles(role)
            await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
    
    @commands.command(name="언뮤트")
    @commands.has_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    async def _unmute(self, ctx, member: discord.Member):
        result = await data.load('guilds', 'guild', ctx.guild.id)
        role = ctx.guild.get_role(int(result[1]))
        if role is not None:
            await member.remove_roles(role)
            await ctx.message.add_reaction("<:cs_yes:659355468715786262>")

    @commands.command(name="슬로우", aliases=["슬로우모드"])
    @commands.has_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    async def _slowmode(self, ctx, numbers: commands.Greedy[int]):
        """
        미야야 슬로우 < 1 ~ 21600 사이의 정수 / 끄기 >


        실행한 채널의 메시지 딜레이를 설정합니다.
        """
        if not numbers:
            if ctx.message.content.split(" ")[2] != "끄기":
                await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 슬로우 < 1 ~ 21600 사이의 정수 / 끄기 >`가 올바른 명령어에요!")
            else:
                await ctx.channel.edit(slowmode_delay=0)
                await ctx.send(f":hourglass: {ctx.author.mention} 채널의 메시지 딜레이를 삭제했어요!")
        else:
            number = numbers[0]
            if number > 21600 or number <= 0:
                await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 슬로우 < 1 ~ 21600 사이의 정수 / 끄기 >`가 올바른 명령어에요!")
            else:
                await ctx.channel.edit(slowmode_delay=number)
                await ctx.send(f":hourglass: {ctx.author.mention} 채널의 메시지 딜레이를 {number}초로 설정했어요!\n \n`채널 관리` 혹은 `메시지 관리` 권한을 가진 사람에게는 적용되지 않아요.\n채널의 메시지 딜레이를 삭제하려면 `미야야 슬로우 끄기` 명령어를 사용해주세요.")

    @commands.command(name="추방")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def _kick(self, ctx, member: discord.Member):
        """
        미야야 추방 < 유저 > [ 사유 ]
        
        
        서버에서 유저를 추방합니다.
        """
        reason = "".join(ctx.message.content.split(" ")[3:])
        try:
            await ctx.guild.kick(member, reason=reason)
            await ctx.message.add_reaction("<:cs_yes:659355468715786262>") 
        except discord.Forbidden:
            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 미야가 추방하려는 유저보다 낮아서 추방하지 못했어요.") 
        
    @commands.command(name="차단")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def _ban(self, ctx, member: discord.Member):
        """
        미야야 차단 < 유저 > [ 사유 ]
        
        
        서버에서 유저를 차단합니다.
        """
        reason = "".join(ctx.message.content.split(" ")[3:])
        try:
            await ctx.guild.ban(member, reason=reason)
            await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
        except discord.Forbidden:
            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 미야가 차단하려는 유저보다 낮아서 차단하지 못했어요.") 
            
    @commands.command(name="청소", aliases=["삭제"])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def _purge(self, ctx, *args):
        """
        미야야 청소 < 1 ~ 100 사이의 정수 >

        
        설정한 갯수 만큼의 메세지를 채널에서 삭제합니다.
        """ 
        if args and args[0].isdecimal() == True:
            num = int(args[0])
            if num <= 100:
                await ctx.message.delete() 
                deleted = await ctx.channel.purge(limit=num)
                await ctx.send(f"<:cs_trash:659355468631769101> {ctx.author.mention} {len(deleted)}개의 메세지를 삭제했어요!", delete_after=3)
            else:
                await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 청소 < 1 ~ 100 사이의 정수 >`가 올바른 명령어에요!")
        else:
            await ctx.send(f"<:cs_console:659355468786958356> {ctx.author.mention} `미야야 청소 < 1 ~ 100 사이의 정수 >`가 올바른 명령어에요!")

def setup(miya):
    miya.add_cog(Moderation(miya))