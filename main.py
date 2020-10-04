import discord
from discord.ext import commands
import koreanbots
from lib import config
from utils import data, webhook


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


miya = Miya(
    command_prefix=commands.when_mentioned_or("미야야 "),
    description="미야 discord.py 리라이트 버전",
    help_command=None,
    fetch_offline_members=True,
    intents=discord.Intents.all(),
)


def load_modules(miya):
    failed = []
    exts = [
        "modules.general",
        "modules.events",
        "modules.settings",
        "modules.devs",
        "modules.mods",
        "modules.support",
        "modules.register",
        "modules.log",
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
    if msg.author.bot:
        return

    if msg.content.startswith("미야야 ") or msg.content.startswith(f"<@{miya.user.id}>") or msg.content.startswith(f"<@!{miya.user.id}>"):
        if "'" not in msg.content and '"' not in msg.content and "\\" not in msg.content:
            result = await data.load("blacklist", "user", msg.author.id)
            if result is not None:
                await webhook.terminal(f"Command Cancelled ( Blacklisted ) : {msg.author} ( {msg.author.id} ) - {msg.content} / Guild : {msg.guild.name} ( {msg.guild.id} )", "미야 Terminal", miya.user.avatar_url)
                print(f"Command Cancelled ( Blacklisted ) : {msg.author} ( {msg.author.id} ) - {msg.content} / Guild : {msg.guild.name} ( {msg.guild.id} )")
                admin = miya.get_user(int(result[1]))
                await msg.channel.send(f"""<a:ban_guy:761149578216603668> {msg.author.mention} 죄송합니다. 당신은 봇 이용이 차단되셨습니다.\n이의제기, 문의는 미야 지원 디스코드에서 하실 수 있습니다. https://discord.gg/mdgaSjB\n사유 : {result[2]}\n처리한 관리자 : {admin}\n차단된 시각 : {result[3]}""")
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
        else:
            await webhook.terminal(f"Command Cancelled ( Banned Word ) : {msg.author} ( {msg.author.id} ) - {msg.content} / Guild : {msg.guild.name} ( {msg.guild.id} )", "미야 Terminal", miya.user.avatar_url)
            print(f"Command Cancelled ( Banned Word ) : {msg.author} ( {msg.author.id} ) - {msg.content} / Guild : {msg.guild.name} ( {msg.guild.id} )")
            await msg.channel.send(f"""<:cs_console:659355468786958356> {msg.author.mention} 미야의 오류 방지를 위해 따옴표와 역슬래시(\\)의 사용을 금지합니다.""")


load_modules(miya)
miya.run(config.BotToken)
