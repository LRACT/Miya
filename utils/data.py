import aiosqlite

async def load(table, find_column, find_value):
    row = None
    async with aiosqlite.connect("lib/miya.sqlite") as o:
        async with o.execute(f"SELECT * FROM {table} WHERE {find_column} = {find_value}") as c:
            rows = await c.fetchall()
            if rows:
                row = rows[0]
    
    return row

async def update(table, column, value, find_column, find_value):
    async with aiosqlite.connect("lib/miya.sqlite") as o:
        try:
            await o.execute(f"UPDATE {table} SET {column} = '{value}' WHERE {find_column} = {find_value}")
        except Exception as e:
            return e
        else:
            return "SUCCESS"

async def insert(table, columns, values):
    async with aiosqlite.connect("lib/miya.sqlite") as o:
        try:
            await o.execute(f"INSERT INTO {table}({columns}), VALUES({values})")
        except Exception as e:
            return e
        else:
            return "SUCCESS"

async def delete(table, find_column, find_value):
    async with aiosqlite.connect('lib/miya.sqlite') as o:
        try:
            await o.execute(f"DELETE FROM {table} WHERE {find_column} = {find_value}")
        except Exception as e:
            return e
        else:
            return "SUCCESS"

