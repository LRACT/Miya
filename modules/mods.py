import discord
from discord.ext import commands
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="추방")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def _kick(self, ctx, member: discord.Member):
        reason = "".join(ctx.message.content.split(" ")[3:])
        try:
            await ctx.guild.kick(member, reason=reason)
            await ctx.message.add_reaction("<:cs_yes:659355468715786262>") 
        except discord.Forbidden:
            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 봇의 권한이 부족해서 명령어를 실행할 수 없어요..") 
        
    @commands.command(name="차단")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def _ban(self, ctx, member: discord.Member):
        reason = "".join(ctx.message.content.split(" ")[3:])
        try:
            await ctx.guild.ban(member, reason=reason)
            await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
        except discord.Forbidden:
            await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} 봇의 권한이 부족해서 명령어를 실행할 수 없어요..") 
            
    @commands.command(name="청소")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def _purge(self, ctx, *args):
        if args and args[0].isdecimal() == True:
            num = int(args[0])
            if num <= 100:
                await ctx.message.delete() 
                deleted = await ctx.channel.purge(limit=num)
                await ctx.send(f"<:cs_trash:659355468631769101> {ctx.author.mention} {len(deleted)}개의 메세지를 삭제하였습니다!", delete_after=3)
            else:
                embed = discord.Embed(description="`미야야 청소 [1~100]`가 올바른 명령어에요!", color=0xFF6060)
                embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.name) 
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description="`미야야 청소 [1~100]`가 올바른 명령어에요!", color=0xFF6060)
            embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.name) 
            await ctx.send(embed=embed)

def setup(miya):
    miya.add_cog(Moderation(miya))