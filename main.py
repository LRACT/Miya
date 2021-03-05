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
    shard_count=5,
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
        "modules.devs",
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
async def _process(ctx):
    await utils.get.process(ctx)

load_modules(miya)
miya.run(config.BotToken)
