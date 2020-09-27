import discord
from discord.ext import commands
from lib import config
from utils import data




miya = commands.Bot(
    command_prefix=commands.when_mentioned_or("미야야 ")
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
    
    if msg.content.startswith("미야야 ") or msg.content.startswith(f"<@{miya.user.id}>") or msg.content.startswith(f"<@!{miya.user.id}>"):
        result = await data.load('blacklist', 'user', msg.author.id)
        if result is not None:
            print(f"Command Cancelled ( Blacklisted ): {msg.author} ( {msg.author.id} ) - {msg.content} / Guild Id: {msg.guild.name} ( {msg.guild.id} )")
            admin = miya.get_user(int(result[1]))
            await msg.channel.send(f"""
            <:cs_stop:665173353874587678> {msg.author.mention} 죄송합니다. 당신은 봇 이용이 차단되셨습니다.
이의제기, 문의는 미야 지원 디스코드에서 하실 수 있습니다. https://discord.gg/mdgaSjB
사유 : {result[2]}
처리한 관리자 : {admin}
차단된 시각 : {result[3]}
            """)
        else:
            g = await data.load('guilds', 'guild', msg.guild.id)
            if g is not None or msg.content == "미야야 등록":
                print(f"Processed Command : {msg.author} ( {msg.author.id} ) - {msg.content}")
                await miya.process_commands(msg)
            else:
                print(f"Command Cancelled ( Guild not registered ) : {msg.author} ( {msg.author.id} ) - {msg.content} / Guild Id: {msg.guild.name} ( {msg.guild.id} )")
                await msg.channel.send(f"<:cs_id:659355469034422282> {msg.author.mention} 아직 미야의 이용약관에 동의하지 않으셨어요. `미야야 등록` 명령어를 사용해 등록해보세요!")

load_modules(miya)
miya.run(config.BotToken)