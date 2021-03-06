import discord 
from discord.ext import commands
import koreanbots
import datetime
from pytz import utc, timezone
from lib import config
from utils import get, data, webhook, exc
import locale
locale.setlocale(locale.LC_ALL, '')

class Miya(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.koreanbots = koreanbots.Client(self, config.DBKRToken)

    async def get_rank(self):
        num = 0
        while True:
            num += 1
            response = await self.koreanbots.getBots(num)
            data = [x.name for x in response]
            if "미야" in data:
                index = data.index("미야")
                result = 9 * (num - 1) + (index + 1)
                return result

intents = discord.Intents(
    guilds=True,
    members=True,
    bans=True,
    emojis=True,
    integrations=True,
    webhooks=True,
    invites=True,
    voice_states=True,
    presences=False,
    messages=True,
    reactions=True, 
    typing=True
)
miya = Miya(
    shard_count=3,
    command_prefix="미야야 ",
    description="다재다능한 Discord 봇, 미야.",
    help_command=None,
    chunk_guilds_at_startup=True,
    intents=intents
)

def load_modules(miya):
    failed = []
    exts = [
        "modules.general",
        "modules.events",
        "modules.settings",
        "modules.admin",
        "modules.mods",
        "modules.register",
        "modules.log",
        "jishaku",
    ]

    for ext in exts:
        try:
            miya.load_extension(ext)
        except Exception as e:
            print(f"{e.__class__.__name__}: {e}")
            failed.append(ext)

    return failed

@miya.event
async def on_message(msg):
    if msg.channel.type == discord.ChannelType.private:
        return

    if msg.author.bot:
        return

    await miya.process_commands(msg)

@miya.check
async def processing(ctx):
    mgr = await get.mgr(ctx)
    f = await get.filter(ctx.message)
    rows = await data.fetch(f"SELECT * FROM `blacklist` WHERE `id` = '{ctx.author.id}'")
    if mgr is True:
        await webhook.terminal(f"Bypassed >\nUser - {ctx.author} ({ctx.author.id})\nContent - {ctx.message.content}\nGuild - {ctx.guild.name} ({ctx.guild.id})", "명령어 처리 기록", miya.user.avatar_url)
        return True
    elif rows:
        admin = miya.get_user(int(rows[0][2]))
        embed = discord.Embed(
            title=f"이런, {ctx.author}님은 차단되셨어요.",
            description=f"""
차단에 관해서는 지원 서버를 방문해주세요.
사유 : {rows[0][1]}
관리자 : {admin}
차단 시각 : {rows[0][3]}
            """,
            timestamp=datetime.datetime.utcnow(),
            color=0xFF3333
        )
        embed.set_author(name="이용 제한", icon_url=miya.user.avatar_url)
        await webhook.terminal(f"Blocked User >\nUser - {ctx.author} ({ctx.author.id})\nContent - {ctx.message.content}\nGuild - {ctx.guild.name} ({ctx.guild.id})", "명령어 처리 기록", miya.user.avatar_url)
        raise exc.Forbidden(embed, ctx)
    elif f[0] is True:
        admin = miya.user
        time = await get.kor_time(datetime.datetime.utcnow())
        await data.commit(f"INSERT INTO `blacklist`(`id`, `reason`, `admin`, `datetime`) VALUES('{ctx.author.id}', '봇 사용 도중 부적절한 언행 **[Auto]** - {f[1]}', '{admin.id}', '{time}')")
        await webhook.blacklist(f"New Block >\nVictim - {ctx.author.id}\nAdmin - {admin} ({admin.id})\nReason - 봇 사용 도중 부적절한 언행 **[Auto]** - {f[1]}", "제한 기록", miya.user.avatar_url)
        embed = discord.Embed(
            title=f"이런, {ctx.author}님은 차단되셨어요.",
            description=f"""
차단에 관해서는 지원 서버를 방문해주세요.
사유 : 봇 사용 도중 부적절한 언행 **[Auto]** - {f[1]}
관리자 : {admin}
차단 시각 : {time}
            """,
            timestamp=datetime.datetime.utcnow(),
            color=0xFF3333
        )
        embed.set_author(name="이용 제한", icon_url=miya.user.avatar_url)
        await webhook.terminal(f"Forbidden >\nUser - {ctx.author} ({ctx.author.id})\nContent - {ctx.message.content}\nGuild - {ctx.guild.name} ({ctx.guild.id})", "명령어 처리 기록", miya.user.avatar_url)
        raise exc.Forbidden(embed, ctx)
    else:
        await webhook.terminal(f"Processed >\nUser - {ctx.author} ({ctx.author.id})\nContent - {ctx.message.content}\nGuild - {ctx.guild.name} ({ctx.guild.id})", "명령어 처리 기록", miya.user.avatar_url)
        return True


load_modules(miya)
miya.run(config.BotToken)
