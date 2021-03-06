import aiomysql
from lib import config
import locale

locale.setlocale(locale.LC_ALL, "")


async def fetch(sql):
    o = await aiomysql.connect(
        host=config.MySQL["host"],
        port=config.MySQL["port"],
        user=config.MySQL["username"],
        password=config.MySQL["password"],
        db=config.MySQL["database"],
        autocommit=True,
    )
    c = await o.cursor()
    try:
        await c.execute(sql)
        rows = await c.fetchall()
        return rows
    except Exception as e:
        return e
    o.close()


async def commit(sql):
    o = await aiomysql.connect(
        host=config.MySQL["host"],
        port=config.MySQL["port"],
        user=config.MySQL["username"],
        password=config.MySQL["password"],
        db=config.MySQL["database"],
        autocommit=True,
    )
    c = await o.cursor()
    try:
        await c.execute(sql)
    except Exception as e:
        return e
    else:
        return "SUCCESS"
    o.close()
