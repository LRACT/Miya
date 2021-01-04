from discord import Webhook, AsyncWebhookAdapter
import aiohttp
from lib import config
import typing
import locale
locale.setlocale(locale.LC_ALL, '')

async def terminal(content, name, avatar):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(config.WebHookURL, adapter=AsyncWebhookAdapter(session))
        await webhook.send(f"```{content}```", username=name, avatar_url=avatar)

async def send(url, content, name: typing.Optional[str] = None, avatar: typing.Optional[str] = None):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
        await webhook.send(content, username=name, avatar_url=avatar)

async def blacklist(content, name, avatar):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(config.BlackURL, adapter=AsyncWebhookAdapter(session))
        await webhook.send(f"```{content}```", username=name, avatar_url=avatar)
