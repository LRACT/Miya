import discord
from discord.ext import commands
import sqlite3

def load_modules(miya):
    failed = []
    exts = [
    "modules.general",
    "modules.events",
    "modules.sexsex",
    "modules.settings",
    "modules.devs",
    "modules.mods"
    ] 

    for ext in exts:
        try:
            miya.load_extension(ext)
        except Exception as e:
            print(f"{e.__class__.__name__}: {e}")
            failed.append(ext)
    
    return failed

if __name__ == "__main__":
    miya = commands.Bot(
        command_prefix=commands.when_mentioned_or("미야야 "), 
        description="미야야 도움을 입력해보세요!",
        )
    load_modules(miya)
    miya.run("Token")