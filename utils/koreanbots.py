import aiohttp

async def get_rank():
    num = 0
    while True:
        num += 1
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://api.koreanbots.dev/bots/get?page={num}') as r:
                response = await r.json()
                data = [x['name'] for x in response['data']]
                if "미야" in data:
                    index = data.index('미야')
                    result = 9 * (num - 1) + (index + 1)
                    return result

