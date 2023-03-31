from Resumeaiogram.app.database.db_connection import Database

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


async def add_id(id):
    await db.connect()
    await db.execute(f'''INSERT INTO public.resume_db1(id) VALUES ('{id}');''')
    await db.disconnect()


async def add_name_surname(id, value):
    await db.connect()
    await db.execute(f'''UPDATE public.resume_db1 SET name_surnme = '{value}' WHERE id = {id};''')
    await db.disconnect()


async def add_phone_number(id, value):
    await db.connect()
    await db.execute(f'''UPDATE public.resume_db1 SET phone_number = '{value}' WHERE id = {id};''')
    await db.disconnect()


async def email(id, value):
    await db.connect()
    await db.execute(f'''UPDATE public.resume_db1 SET email = '{value}' WHERE id = {id};''')
    await db.disconnect()


async def education(id, value):
    await db.connect()
    await db.execute(f'''UPDATE public.resume_db1 SET education = '{value}' WHERE id = {id};''')
    await db.disconnect()

