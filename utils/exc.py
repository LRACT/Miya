import discord
from discord.ext import commands


class Forbidden(commands.CheckFailure):
    def __init__(self, embed, ctx):
        self.embed = embed
        super().__init__(
            "<a:ban_guy:761149578216603668> https://discord.gg/tu4NKbEEnn")


class Forbidden(commands.CheckFailure):
    def __init__(self, ctx):
        super().__init__(
            "<:cs_id:659355469034422282> 미야와 대화하시려면, 먼저 이용 약관에 동의하셔야 해요.\n`미야야 가입` 명령어를 사용해보세요!"
        )
