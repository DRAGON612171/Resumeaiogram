from aiogram import types, Dispatcher, Bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from steps import *
from keyboards import *
from config import *


bot = Bot(token=Token)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id, '👋Привіт!👋\n'  
                                            '😃Це бот для створення резюме, думаю тобі сподобається😃'.format(message.from_user.first_name), reply_markup=but_create())

# def but_create():
#     reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
#     but1 = KeyboardButton('📄Створити резюме📄')
#     reply_markup.add(but1)
#     return reply_markup
@dp.message_handler(content_types=['text'])
async def name_surname(message: types.Message):
    if message.text == '📄Створити резюме📄':
        reply_markup1 = ReplyKeyboardMarkup(resize_keyboard=True)
        await message.answer('Напишіть ваше ім’я і прізвище', reply_markup=reply_markup1)
        await Steps.name_surname.set()

@dp.message_handler(content_types=['text'], state=Steps.name_surname)
async def name_surname2(message: types.Message):
    item = message.text
    print('name_surname {}'.format(item))
    await Steps.phone_number.set()
    await message.answer('Напишіть ваш номер телефону')


@dp.message_handler(content_types=['text'], state=Steps.phone_number)
async def phone_number(message: types.Message):
    phone_number = message.text
    print('phone_number {}'.format(phone_number))
    await Steps.get_email.set()
    await message.answer('Напишіть ваш email')


@dp.message_handler(state=Steps.get_email)
async def get_email (message: types.Message):
    get_email = message.text
    print('email {}'.format(get_email))
    await Steps.get_education.set()
    await message.answer('Напишіть рівень вашої освіти')
@dp.message_handler(state=Steps.get_education)
async def get_education(message: types.Message):
    get_education = message.text
    print('education {}'.format(get_education))
    await Steps.get_tech_skills.set()
    await message.answer('Напишіть ваші Tech Skills')
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
    get_lang = message.text
    print('lang {}'.format(get_lang))
    await Steps.get_lang_level.set()
    await message.answer('Напишіть рівень знання цих мов')


@dp.message_handler(state=Steps.get_lang_level)
async def get_lang(message: types.Message):
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
    # await message.answer("😎Ваше резюме готове, перевірте свої дані:😎\n"
    #                      f"Ім'я та прізивще: {name_surname}\n"
    #                      f"Номер телефону: {phone_number}\n"
    #                      f"Електронна пошта: {get_email}\n"
    #                      f"Освіта: {get_education}\n"
    #                      f"Tech Навички: {get_tech_skills}\n"
    #                      f"Soft Навички: {get_soft_skills}\n"
    #                      f"Посилання на ваші проекти: \n"
    #                      f"Мови: {get_lang}\n"
    #                      f"Рівень знання цих мов:\n"
    #                      f"Ваша країна: {get_country}\n"
    #                      f"Ваше місто: {get_city}\n"
    #                      f"Посада на яку претендуєте: {get_profession}\n"
    #                      f"Ваші очікування від роботи: {get_description}\n"
    #                      f"Ваш минулий досвід роботи(минула посада): {get_work_experience}\n"
    #                      f"Що ви робили на цій посаді: {get_job_description}\n"
    #                      f"Скільки часу ви займали цю посаду: {get_how_long}\n"
    #                      "Чи хочете відредагувати свої дані?'\n")










if __name__ == '__main__':
    executor.start_polling(dp)