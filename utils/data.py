import aiomysql
from lib import config

async def load(table, find_column, find_value):
    o = await aiomysql.connect(
        host=config.MySQL['host'],
        port=config.MySQL['port'],
        user=config.MySQL['username'],
        password=config.MySQL['password'],
        db=config.MySQL['database'],
        autocommit=True
    )
    c = await o.cursor()
    await c.execute(f"SELECT * FROM `{table}` WHERE `{find_column}` = '{find_value}'")
    rows = await c.fetchall()
    if rows:
        if len(rows) == 1:
            return rows[0]
        else:
            return rows
    else:
        return None
    o.close()

async def update(table, column, value, find_column, find_value):
    o = await aiomysql.connect(
        host=config.MySQL['host'],
        port=config.MySQL['port'],
        user=config.MySQL['username'],
        password=config.MySQL['password'],
        db=config.MySQL['database'],
        autocommit=True
    )
    c = await o.cursor()
    try:
        await c.execute(f"UPDATE `{table}` SET `{column}` = '{value}' WHERE `{find_column}` = '{find_value}'")
    except Exception as e:
        return e
    else:
        return "SUCCESS"
    o.close()

async def insert(table, columns, values):
    o = await aiomysql.connect(
        host=config.MySQL['host'],
        port=config.MySQL['port'],
        user=config.MySQL['username'],
        password=config.MySQL['password'],
        db=config.MySQL['database'],
        autocommit=True
    )
    c = await o.cursor()
    try:
        await c.execute(f"INSERT INTO `{table}`({columns}) VALUES({values})")
    except Exception as e:
        return e
    else:
        return "SUCCESS"
    o.close()

async def delete(table, find_column, find_value):
    o = await aiomysql.connect(
        host=config.MySQL['host'],
        port=config.MySQL['port'],
        user=config.MySQL['username'],
        password=config.MySQL['password'],
        db=config.MySQL['database'],
        autocommit=True
    )
    c = await o.cursor()
    try:
        await c.execute(f"DELETE FROM `{table}` WHERE `{find_column}` = '{find_value}'")
    except Exception as e:
        return e
    else:
        return "SUCCESS"
    o.close()

