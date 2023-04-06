import asyncpg
from Resumeaiogram import config
from Resumeaiogram.database.db_connection import Database

# from app.database.db_connection import Database

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


async def add_email(id, value):
    await db.connect()
    await db.execute(f'''UPDATE public.resume_db1 SET email = '{value}' WHERE id = {id};''')
    await db.disconnect()


async def add_education(id, value):
    await db.connect()
    await db.execute(f'''UPDATE public.resume_db1 SET education = '{value}' WHERE id = {id};''')
    await db.disconnect()


async def add_lang(id, value):
    await db.connect()
    await db.execute(f'''UPDATE public.resume_db1 SET lang = '{value}' WHERE id = {id};''')
    await db.disconnect()


async def add_lang_level(id, value):
    await db.connect()
    await db.execute(f'''UPDATE public.resume_db1 SET lang_level = '{value}' WHERE id = {id};''')
    await db.disconnect()


async def add_country(id, value):
    await db.connect()
    await db.execute(f'''UPDATE public.resume_db1 SET country = '{value}' WHERE id = {id};''')
    await db.disconnect()


async def add_city(id, value):
    await db.connect()
    await db.execute(f'''UPDATE public.resume_db1 SET city = '{value}' WHERE id = {id};''')
    await db.disconnect()


async def add_description(id, value):
    await db.connect()
    await db.execute(f'''UPDATE public.resume_db1 SET description = '{value}' WHERE id = {id};''')
    await db.disconnect()


async def add_profession(id, value):
    await db.connect()
    await db.execute(f'''UPDATE public.resume_db1 SET profession = '{value}' WHERE id = {id};''')
    await db.disconnect()


async def add_soft_skills(id, value):
    await db.connect()
    await db.execute(f'''UPDATE public.resume_db1 SET soft_skills = '{value}' WHERE id = {id};''')
    await db.disconnect()


async def add_tech_skills(id, value):
    await db.connect()
    await db.execute(f'''UPDATE public.resume_db1 SET tech_skills = '{value}' WHERE id = {id};''')
    await db.disconnect()


async def add_projects(id, value):
    await db.connect()
    await db.execute(f'''UPDATE public.resume_db1 SET projects = '{value}' WHERE id = {id};''')
    await db.disconnect()


async def add_how_long(id, value):
    await db.connect()
    await db.execute(f'''UPDATE public.resume_db1 SET how_long = '{value}' WHERE id = {id};''')
    await db.disconnect()


async def add_job_description(id, value):
    await db.connect()
    await db.execute(f'''UPDATE public.resume_db1 SET job_description = '{value}' WHERE id = {id};''')
    await db.disconnect()


async def add_past_work(id, value):
    await db.connect()
    await db.execute(f'''UPDATE public.resume_db1 SET past_work = '{value}' WHERE id = {id};''')
    await db.disconnect()


async def add_password(id, value):
    await db.connect()
    await db.execute(f'''UPDATE public.resume_db1 SET password = '{value}' WHERE id = {id};''')
    await db.disconnect()


async def clear_table(id):
    await db.connect()
    await db.execute(f'''UPDATE public.resume_db1
    SET name_surname=0, phone_number=0, email=0, education=0, lang=0, lang_level=0, country=0, city=0, description=0,
    profession=0, soft_skills=0, tech_skills=0, projects=0, how_long=0, job_description=0, past_work=0
    WHERE id={id};''')
    await db.disconnect()
