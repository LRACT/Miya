import discord
from discord.ext import commands
import sqlite3

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

if __name__ == "__main__":
    miya = commands.Bot(
        command_prefix=commands.when_mentioned_or("청정수 "), 
        description="미야 discord.py 리라이트 버전",
        )
    load_modules(miya)
    miya.run("Token")
