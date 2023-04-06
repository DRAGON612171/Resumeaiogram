# import asyncio

from aiogram import types, Dispatcher, Bot
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import edit_answers
#from app.database import db_executions

from Resumeaiogram import config
from Resumeaiogram.database import db_executions
# from app.database import db_executions
from steps import *
from keyboards import *

bot = Bot(token=config.Token)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id, '👋Привіт!👋\n'  
                                            '😃Це бот для створення резюме, думаю тобі сподобається😃'.format(message.from_user.first_name), reply_markup=but_create)
    #await db_executions.add_id(message.chat.id)


@dp.message_handler(content_types=['text'])
async def name_surname(message: types.Message):
    if message.text == '📄Створити резюме📄':
        reply_markup1 = ReplyKeyboardMarkup(resize_keyboard=True)
        await message.answer('Напишіть ваше ім’я і прізвище', reply_markup=reply_markup1)
        await Steps.name_surname.set()


@dp.message_handler(content_types=['text'], state=Steps.name_surname)
async def name_surname2(message: types.Message):
    #await db_executions.add_name_surname(message.chat.id, message.text)
    print('name_surname {}'.format(message.text))
    await Steps.phone_number.set()
    await message.answer('Напишіть ваш номер телефону')


@dp.message_handler(content_types=['text'], state=Steps.phone_number)
async def phone_number(message: types.Message):
    phone_number = message.text
    print('phone_number {}'.format(phone_number))
    await Steps.get_email.set()
    await message.answer('Напишіть ваш email')


@dp.message_handler(state=Steps.get_email)
async def get_email(message: types.Message):
    get_email = message.text
    print('email {}'.format(get_email))
    await Steps.get_education.set()
    await message.answer('Напишіть рівень вашої освіти')


@dp.message_handler(state=Steps.get_education)
async def get_education(message: types.Message):
    education_list = []
    if message.text.lower() == 'stop':
        await Steps.get_tech_skills.set()
        await message.answer('Напишіть ваші Tech Skills')
    else:
        education_list.append(message.text)
        await message.answer('Напишіть рівень вашої освіти', reply_markup=lists)
        print(education_list)


@dp.message_handler(state=Steps.get_tech_skills)
async def get_tech_skills(message: types.Message):
    get_tech_skills = message.text
    print('tech skills {}'.format(get_tech_skills))
    await Steps.get_soft_skills.set()
    await message.answer('Напишіть ваші Soft Skills')


@dp.message_handler(state=Steps.get_soft_skills)
async def get_soft_skills (message: types.Message()):
    get_soft_skills = message.text
    print('soft skills {}'.format(get_soft_skills))
    await Steps.get_projects.set()
    await message.answer('Додайте посилання на ваші проекти')


@dp.message_handler(state=Steps.get_projects)
async def get_soft_skills(message: types.Message):
    get_projects = message.text
    print('projects {}'.format(get_projects))
    await Steps.get_lang.set()
    await message.answer('Напишіть з які ви знаєте мови')


@dp.message_handler(state=Steps.get_lang)
async def get_lang(message: types.Message):
    get_lang = '1,2,3'
    print('lang {}'.format(get_lang))
    await Steps.get_lang_level.set()
    await message.answer('Напишіть рівень знання цiєї мови')

#UPDATE public.qwert
#SET name2=array_append(name2, 'Nazar')
#WHERE id = 1;

@dp.message_handler(state=Steps.get_lang_level)
async def get_lang_level(message: types.Message):
    get_lang_level = message.text
    print('lang_level {}'.format(get_lang_level))
    await Steps.get_country.set()
    await message.answer('Напишіть з якої ви країни')


@dp.message_handler(state=Steps.get_country)
async def get_country(message: types.Message):
    get_country = message.text
    print('country {}'.format(get_country))
    await Steps.get_city.set()
    await message.answer('Напишіть з якого ви міста')


@dp.message_handler(state=Steps.get_city)
async def get_city(message: types.Message):
    get_city = message.text
    print('city {}'.format(get_city))
    await Steps.get_profession.set()
    await message.answer('Напишіть на яку посаду претендуєте')


@dp.message_handler(state=Steps.get_profession)
async def get_profession(message: types.Message):
    get_profession = message.text
    print('profession {}'.format(get_profession))
    await Steps.get_description.set()
    await message.answer('Напишіть, що ви очікуєте від цієї посади(можете розповісти щось про себе')


@dp.message_handler(state=Steps.get_description)
async def get_description(message: types.Message):
    get_descreption = message.text
    print('descreption {}'.format(get_descreption))
    await Steps.get_work_experience.set()
    await message.answer('Напишіть про ваш минулий досвід роботи(назва посади)')


@dp.message_handler(state=Steps.get_work_experience)
async def get_work_experience(message: types.Message):
    get_work_experience = message.text
    print('work_experience {}'.format(get_work_experience))
    await Steps.get_job_description.set()
    await message.answer('Опишіть, що робили на цій роботі')


@dp.message_handler(state=Steps.get_job_description)
async def get_job_description(message: types.Message):
    get_job_description = message.text
    print('get_job_description {}'.format(get_job_description))
    await Steps.get_how_long.set()
    await message.answer('Скільки часу ви займали цю посаду?')


@dp.message_handler(state=Steps.get_how_long)
async def get_how_long(message: types.Message):
    get_how_long = message.text
    print('get_how_long {}'.format(get_how_long))
    result = await db_executions.select_all()
    right_user = ''
    for data_tuple in result:
        if int(message.chat.id) in data_tuple:
            right_user = data_tuple
    await message.answer("😎Ваше резюме готове, перевірте свої дані:😎\n"
                         f"Ім'я та прізивще: {right_user[1]}\n"
                         f"Номер телефону: {right_user[2]}\n"
                         f"Електронна пошта: {right_user[3]}\n"
                         f"Освіта: {right_user[4]}\n"
                         f"Tech Навички: {right_user[-5]}\n"
                         f"Soft Навички: {right_user[-6]}\n"
                         f"Посилання на ваші проекти: {right_user[-4]}\n"
                         f"Мови: {right_user[5]}\n"
                         f"Рівень знання цих мов:{right_user[6]}\n"
                         f"Ваша країна: {right_user[7]}\n"
                         f"Ваше місто: {right_user[8]}\n"
                         f"Посада на яку претендуєте: {right_user[11]}\n"
                         f"Ваші очікування від роботи: {right_user[10]}\n"
                         f"Ваш минулий досвід роботи(минула посада): {right_user[-1]}\n"
                         f"Що ви робили на цій посаді: {right_user[-2]}\n"
                         f"Скільки часу ви займали цю посаду: {right_user[-3]}\n"
                         "Чи хочете відредагувати свої дані?'\n", reply_markup=changes)


@dp.callback_query_handler(state='*')
async def bot_drop_wheel(callback: types.callback_query):
    if callback == 'name_surname':
        await bot.send_message(callback.from_user.id, "Введіть нове значення:")
        await edit_answers.edit_name_surname()
    elif callback == 'phone':
        await bot.send_message(callback.from_user.id, "Введіть нове значення:")
        await edit_answers.edit_phone_number()
    if callback == 'email':
        await bot.send_message(callback.from_user.id, "Введіть нове значення:")
        await edit_answers.edit_email()
    elif callback == 'education':
        await bot.send_message(callback.from_user.id, "Введіть нове значення:")
        await edit_answers.edit_education()
    if callback == 'soft_skills':
        await bot.send_message(callback.from_user.id, "Введіть нове значення:")
        await edit_answers.edit_soft_skills()
    elif callback == 'tech_skills':
        await bot.send_message(callback.from_user.id, "Введіть нове значення:")
        await edit_answers.edit_tech_skills()
    if callback == 'projects':
        await bot.send_message(callback.from_user.id, "Введіть нове значення:")
        await edit_answers.edit_projects()
    elif callback == 'lang':
        await bot.send_message(callback.from_user.id, "Введіть нове значення:")
        await edit_answers.edit_lang()
    if callback == 'lang_level':
        await bot.send_message(callback.from_user.id, "Введіть нове значення:")
        await edit_answers.edit_lang_level()
    elif callback == 'country':
        await bot.send_message(callback.from_user.id, "Введіть нове значення:")
        await edit_answers.edit_country()
    if callback == 'city':
        await bot.send_message(callback.from_user.id, "Введіть нове значення:")
        await edit_answers.edit_city()
    elif callback == 'profession':
        await bot.send_message(callback.from_user.id, "Введіть нове значення:")
        await edit_answers.edit_profession()
    if callback == 'description':
        await bot.send_message(callback.from_user.id, "Введіть нове значення:")
        await edit_answers.edit_description()
    elif callback == 'past_work':
        await bot.send_message(callback.from_user.id, "Введіть нове значення:")
        await edit_answers.edit_past_work()
    if callback == 'job_description':
        await bot.send_message(callback.from_user.id, "Введіть нове значення:")
        await edit_answers.edit_job_description()
    elif callback == 'how_long':
        await bot.send_message(callback.from_user.id, "Введіть нове значення:")
        await edit_answers.edit_how_long()










if __name__ == '__main__':
    executor.start_polling(dp)
