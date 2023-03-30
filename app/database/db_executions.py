from .db_connection import Database
import asyncio


db = Database()


#Кожну функцію треба робити через asyncio.run(select_all())
async def select_all():
    await db.connect()

    # Выполнение запроса на чтение
    result = await db.fetch('SELECT * FROM resume_db')

    right_values = []
    for row in result:
        right_values.append(tuple(row))
    print(right_values)

    # Отключение от базы данных
    await db.disconnect()
    return right_values
