import aiosqlite

async def base_work(db_file, input):
    async with aiosqlite.connect(db_file) as db:
        async with db.cursor() as cursor:
            await cursor.execute(input)
            await db.commit()
            results = await cursor.fetchall()
    return results
