import aiosqlite

async def load(guild_id, table):
    row = None
    async with aiosqlite.connect("miya.sqlite") as o:
        async with o.execute(f"SELECT * FROM {table} WHERE guild = {guild_id}") as c:
            rows = await c.fetchall()
            if rows:
                row = rows[0]
    
    return row

async def commit(guild_id, table, column, value):
    async with aiosqlite.connect("miya.sqlite") as o:
        try:
            await o.execute(f"UPDATE {table} SET {column} = '{value}' WHERE guild = {guild_id}")
        except Exception as e:
            return e
        else:
            return "SUCCESS"


