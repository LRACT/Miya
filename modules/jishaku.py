from discord.ext import commands

from jishaku.cog import STANDARD_FEATURES, OPTIONAL_FEATURES

class Jishaku(*OPTIONAL_FEATURES, *STANDARD_FEATURES):
    pass

def setup(miya):
    bot.add_cog(Jishaku(miya))