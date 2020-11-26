import discord
from discord.ext import commands
import koreanbots
import datetime
from pytz import utc, timezone
from lib import config
import utils
from utils import data, webhook
import locale
locale.setlocale(locale.LC_ALL, '')

class Miya(commands.Bot):
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
    command_prefix=commands.when_mentioned_or("미야야 "),
    description="미야 discord.py 리라이트 버전",
    help_command=None,
    fetch_offline_members=True,
    intents=intents
)

def load_modules(miya):
    failed = []
    exts = [
        "modules.general",
        "modules.events",
        "modules.settings",
        "modules.devs",
        "modules.mods",
        "modules.register",
        "modules.log",
        "modules.private",
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

    if msg.content.startswith("미야야 ") or msg.content.startswith(f"<@{miya.user.id}> ") or msg.content.startswith(f"<@!{miya.user.id}> "):
        if msg.content.startswith("미야야 실행") or msg.content.startswith(f"<@{miya.user.id}> 실행") or msg.content.startswith(f"<@!{miya.user.id}> 실행"):
            await webhook.terminal(f"Processed Command : {msg.author} ( {msg.author.id} ) - {msg.content} / Guild : {msg.guild.name} ( {msg.guild.id} )", "미야 Terminal", miya.user.avatar_url)
            print(f"Processed Command : {msg.author} ( {msg.author.id} ) - {msg.content} / Guild : {msg.guild.name} ( {msg.guild.id} )")
            await miya.process_commands(msg)
        elif "'" in msg.content or '"' in msg.content or "\\" in msg.content:
            await webhook.terminal(f"Command Cancelled ( Banned Word ) : {msg.author} ( {msg.author.id} ) - {msg.content} / Guild : {msg.guild.name} ( {msg.guild.id} )", "미야 Terminal", miya.user.avatar_url)
            print(f"Command Cancelled ( Banned Word ) : {msg.author} ( {msg.author.id} ) - {msg.content} / Guild : {msg.guild.name} ( {msg.guild.id} )")
            await msg.channel.send(f"""<:cs_console:659355468786958356> {msg.author.mention} 미야의 오류 방지를 위해 따옴표와 역슬래시의 사용을 금지합니다.""")
        else:
            result = await data.load("blacklist", "id", msg.author.id)
            fbd = await utils.get.filter()
            if result is not None:
                await webhook.terminal(f"Command Cancelled ( Blacklisted ) : {msg.author} ( {msg.author.id} ) - {msg.content} / Guild : {msg.guild.name} ( {msg.guild.id} )", "미야 Terminal", miya.user.avatar_url)
                print(f"Command Cancelled ( Blacklisted ) : {msg.author} ( {msg.author.id} ) - {msg.content} / Guild : {msg.guild.name} ( {msg.guild.id} )")
                admin = miya.get_user(int(result[1]))
                embed = discord.Embed(title="이런, 당신은 미야 사용이 제한되었어요!", description=f"제한에 관한 내용은 [지원 서버](https://discord.gg/mdgaSjB)로 문의해주세요.\n사유 : {result[2]}\n처리한 관리자 : {admin}\n차단된 시각 : {result[3]}", color=0xFF0000)
                await msg.channel.send(f"<a:ban_guy:761149578216603668> {msg.author.mention} https://discord.gg/mdgaSjB", embed=embed)
            elif fbd[0] == True:
                KST = timezone('Asia/Seoul')
                now = datetime.datetime.utcnow()
                time = utc.localize(now).astimezone(KST)
                time = time.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
                await webhook.terminal(f"Command Cancelled ( Forbidden ) : {msg.author} ( {msg.author.id} ) - {msg.content} / Guild : {msg.guild.name} ( {msg.guild.id} )", "미야 Terminal", miya.user.avatar_url)
                print(f"Command Cancelled ( Forbidden ) : {msg.author} ( {msg.author.id} ) - {msg.content} / Guild : {msg.guild.name} ( {msg.guild.id} )")
                result = await data.insert('blacklist', '`id`, `admin`, `reason`, `datetime`', f"'{msg.author.id}', '{miya.user.id}', '부적절한 단어 사용 **[ 미야 자동 차단 ]**', '{time}'")
                if result == "SUCCESS":
                    embed = discord.Embed(title="이런, 당신은 미야 사용이 제한되었어요!", description=f"제한에 관한 내용은 [지원 서버](https://discord.gg/mdgaSjB)로 문의해주세요.\n사유 : 부적절한 단어 사용 [ 미야 자동 차단 ] - {fbd[1]}\n처리한 관리자 : {miya.user}", color=0xFF0000)
                    await msg.channel.send(f"<a:ban_guy:761149578216603668> {msg.author.mention} https://discord.gg/mdgaSjB", embed=embed)
            else:
                g = await data.load("guilds", "guild", msg.guild.id)
                if g is not None or msg.content == "미야야 등록":
                    await webhook.terminal(f"Processed Command : {msg.author} ( {msg.author.id} ) - {msg.content} / Guild : {msg.guild.name} ( {msg.guild.id} )", "미야 Terminal", miya.user.avatar_url)
                    print(f"Processed Command : {msg.author} ( {msg.author.id} ) - {msg.content} / Guild : {msg.guild.name} ( {msg.guild.id} )")
                    await miya.process_commands(msg)
                else:
                    await webhook.terminal(f"Command Cancelled ( Guild not registered ) : {msg.author} ( {msg.author.id} ) - {msg.content} / Guild : {msg.guild.name} ( {msg.guild.id} )", "미야 Terminal", miya.user.avatar_url)
                    print(f"Command Cancelled ( Guild not registered ) : {msg.author} ( {msg.author.id} ) - {msg.content} / Guild : {msg.guild.name} ( {msg.guild.id} )")
                    await msg.channel.send(f"<:cs_id:659355469034422282> {msg.author.mention} 아직 미야의 이용약관에 동의하지 않으셨어요. `미야야 등록` 명령어를 사용해 등록해보세요!")

load_modules(miya)
miya.run(config.BotToken)