from discord import Webhook, AsyncWebhookAdapter
import aiohttp
from lib import config

async def send(content, name, avatar):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(config.WebHookURL, adapter=AsyncWebhookAdapter(session))
        await webhook.send(content, username=name, avatar_url=avatar)