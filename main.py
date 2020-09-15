import discord
from discord.ext import commands
from lib import config
from utils import data




miya = commands.Bot(
    command_prefix=commands.when_mentioned_or("청정수 ")
    # description="미야 discord.py 리라이트 버전",
    )
miya.remove_command('help')

def load_modules(miya):
    failed = []
    exts = [
        "modules.general",
        "modules.events",
        "modules.settings",
        "modules.devs",
        "modules.mods",
        'modules.support'
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
    
    if msg.content.startswith("청정수 ") or msg.content.startswith(f"<@{miya.user.id}>") or msg.content.startswith(f"<@!{miya.user.id}>"):
        result = await data.load('blacklist', 'user', msg.author.id)
        if result is not None:
            print(f"Command Cancelled : {msg.author} ( {msg.author.id} ) - {msg.content}\nGuild Id: {msg.guild.name} ( {msg.guild.id} )\n")
            admin = miya.get_user(int(result[1]))
            await msg.channel.send(f"""
                :hammer: {msg.author.mention} 죄송합니다. 당신은 봇 이용이 차단되셨습니다.
                이의제기, 문의는 미야 지원 디스코드에서 하실 수 있습니다. https://discord.gg/mdgaSjB
                사유 : {result[2]}
                처리한 관리자 : {admin}
                차단된 시각 : {result[3]}
            """)
        else:
            print(f"Processed Command : {msg.author} ( {msg.author.id} ) - {msg.content}")
            await miya.process_commands(msg)

load_modules(miya)
miya.run(config.BotToken)