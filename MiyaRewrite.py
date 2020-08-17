import discord
from discord import commands
import sqlite3



miya = commands.Bot(command_prefix=commands.when_mentioned_or("미야야"), description="다재다능한 관리 봇, 미야.")



miya.run("Token")
