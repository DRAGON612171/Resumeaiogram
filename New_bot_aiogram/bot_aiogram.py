import random
import string

from aiogram import types, Dispatcher, Bot
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

#import config
# from Resumeaiogram.New_bot_aiogram import edit_answers
# from Resumeaiogram.app.database import db_executions
from Resumeaiogram import config

import edit_answers
#from app.database import db_executions
from admins_notify import notify_admins
#from database import db_executions

# from Resumeaiogram import config
from Resumeaiogram.database import db_executions

# from app.database import db_executions
from steps import *
from keyboards import *

bot = Bot(token=config.Token)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['instruction'], state='*')
async def instruction(message: types.Message):
    await bot.send_message(message.chat.id, 'Тут все просто) \n'
                                            'Всі данні слід записувати через кому, а коли побачите "🔴",'
                                            'то треба вводити свої данні по одному, тобто один пункт'
                                            ' в одному повідомленні.\n'
                                            'Пропонуємо спочатку передивитися приклад заповнення: /example')


@dp.message_handler(commands=['example'], state='*')
async def example(message: types.Message):
    photo = open('resume_example.jpg', 'rb')
    await bot.send_message(message.chat.id, 'Ось приклад заповнення резюме:')
    await bot.send_photo(message.chat.id, photo=photo)


@dp.message_handler(commands=['clear'], state='*')
async def clear(message: types.Message):
    await bot.send_message(message.chat.id, 'Ви впевнені, що хочете видалити всі данні?', reply_markup=confirm)


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message):
    try:
        await db_executions.add_id(message.chat.id)
    except:
        pass
    await bot.send_message(message.chat.id, '👋Привіт!👋\n'  
                                            '😃Це бот для створення резюме, думаю тобі сподобається😃 \n'
                                            'Якщо ви вперше складаєте резюме, то ознайомтеся як це краще зробити: \n'
                                            '/instruction \n'
                                            '/example'.format(message.from_user.first_name), reply_markup=but_create)


@dp.message_handler(content_types=['text'])
async def create_resume(message: types.Message):
    if message.text == '📄Створити резюме📄':
        reply_markup1 = ReplyKeyboardMarkup(resize_keyboard=True)
        await message.answer('Напишіть ваше ім’я і прізвище', reply_markup=reply_markup1)
        await Steps.name_surname.set()


@dp.message_handler(content_types=['text'], state=Steps.name_surname)
async def name_surname(message: types.Message):
    try:
        await db_executions.add_name_surname(message.chat.id, message.text)
        print('name_surname {}'.format(message.text))
        await Steps.phone_number.set()
        await message.answer('Напишіть ваш номер телефону')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(content_types=['text'], state=Steps.phone_number)
async def phone_number(message: types.Message):
    try:
        await db_executions.add_phone_number(message.chat.id, message.text)
        print('phone_number {}'.format(phone_number))
        await Steps.get_email.set()
        await message.answer('Напишіть ваш email')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_email)
async def get_email(message: types.Message):
    try:
        await db_executions.add_email(message.chat.id, message.text)
        print('email {}'.format(get_email))
        await Steps.get_education.set()
        await message.answer('Напишіть рівень вашої освіти')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_education)
async def get_education(message: types.Message):
    try:
        await db_executions.add_education(message.chat.id, message.text)
        await message.answer('Напишіть ваші Tech Skills')
        await Steps.get_tech_skills.set()
        print(get_education)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_tech_skills)
async def get_tech_skills(message: types.Message):
    try:
        await db_executions.add_tech_skills(message.chat.id, message.text)
        print('tech skills {}'.format(get_tech_skills))
        await Steps.get_soft_skills.set()
        await message.answer('Напишіть ваші Soft Skills')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_soft_skills)
async def get_soft_skills(message: types.Message()):
    try:
        await db_executions.add_soft_skills(message.chat.id, message.text)
        print('soft skills {}'.format(get_soft_skills))
        await Steps.get_projects.set()
        await message.answer('Додайте посилання на ваші проекти')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_projects)
async def get_projects(message: types.Message):
    try:
        await db_executions.add_projects(message.chat.id, message.text)
        get_projects = message.text
        print('projects {}'.format(get_projects))
        await Steps.get_lang.set()
        await message.answer('Напишіть яку ви знаєте мову🔴')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_lang)
async def get_lang(message: types.Message):
    try:
        if message.text.lower() == 'stop':
            await Steps.get_country.set()
            await message.answer('Напишіть з якої ви країни')
        else:
            await db_executions.add_lang(message.chat.id, message.text)
            print('lang{}'.format(get_lang))
            await Steps.get_lang_level.set()
            await message.answer('Напишіть рівень мови🔴', reply_markup=lists)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_lang_level)
async def get_lang_level(message: types.Message):
    try:
        if message.text.lower() == 'stop':
            await Steps.get_country.set()
            await message.answer('Напишіть з якої ви країни')
        else:
            await db_executions.add_lang_level(message.chat.id, message.text)
            print('lang_level {}'.format(get_lang_level))
            await Steps.get_lang.set()
            await message.answer('Напишіть яку ви знаєте мову')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_country)
async def get_country(message: types.Message):
    try:
        await db_executions.add_country(message.chat.id, message.text)
        print('country {}'.format(get_country))
        await Steps.get_city.set()
        await message.answer('Напишіть з якого ви міста')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_city)
async def get_city(message: types.Message):
    try:
        await db_executions.add_city(message.chat.id, message.text)
        print('city {}'.format(get_city))
        await Steps.get_profession.set()
        await message.answer('Напишіть на яку посаду претендуєте')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_profession)
async def get_profession(message: types.Message):
    try:
        await db_executions.add_profession(message.chat.id, message.text)
        print('profession {}'.format(get_profession))
        await Steps.get_description.set()
        await message.answer('Напишіть, що ви очікуєте від цієї посади(можете розповісти щось про себе')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_description)
async def get_description(message: types.Message):
    try:
        await db_executions.add_description(message.chat.id, message.text)
        print('description {}'.format(get_description))
        await Steps.get_work_experience.set()
        await message.answer('Напишіть про ваш минулий досвід роботи(назва посади)🔴')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_work_experience)
async def get_work_experience(message: types.Message):
    try:
        if message.text.lower() == 'stop':
            await Steps.end_message.set()
            await message.answer('😎Ваше резюме готове, перевірте свої дані:😎')
        else:
            await db_executions.add_past_work(message.chat.id, message.text)
            print('get_work_experience {}'.format(get_work_experience))
            await Steps.get_job_description.set()
            await message.answer('Опишіть, що робили на цій роботі🔴', reply_markup=lists)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_job_description)
async def get_job_description(message: types.Message):
    try:
        if message.text.lower() == 'stop':
            await Steps.end_message.set()
            await message.answer('😎Ваше резюме майже готове, перевірте свої дані:😎')
        else:
            await db_executions.add_job_description(message.chat.id, message.text)
            print('get_job_description {}'.format(get_job_description))
            await Steps.get_how_long.set()
            await message.answer('Скільки часу ви займали цю посаду?🔴', reply_markup=lists)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_how_long)
async def get_how_long(message: types.Message):
    try:
        if message.text.lower() == 'stop':
            await Steps.end_message.set()
            await message.answer('😎Ваше резюме готове, перевірте свої дані:😎')
        else:
            await db_executions.add_how_long(message.chat.id, message.text)
            print('get_how_long {}'.format(get_how_long))
            await Steps.get_work_experience.set()
            await message.answer('Напишіть про ваш минулий досвід роботи(назва посади)🔴', reply_markup=lists)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.end_message)
async def end_message(message: types.Message):
    result = await db_executions.select_all()
    right_user = ''
    for data_tuple in result:
        if int(message.chat.id) in data_tuple:
            right_user = data_tuple
    await message.answer(f"Ім'я та прізивще: {right_user[1]}\n"
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
                         "Чи хочете відредагувати свої дані?'\n", reply_markup=end_keyboard)


@dp.callback_query_handler(state='*')
async def bot_changes(callback: types.callback_query):
    if callback.data == '15':
        await bot.send_message(callback.from_user.id, "Що бажаєте змінити?", reply_markup=changes)
    elif callback.data == '16':
        await db_executions.add_password(callback.chat.id)
        await bot.send_message(callback.from_user.id, "Все готово, можете зайти до сайту і отримати своє резюме:")
        #Додати посилання на сайт
        # await bot.send_message(callback.from_user.id, "")

    if callback.data == 'name_surname':
        await bot.send_message(callback.from_user.id, "Нове нове прізвище та ім'я")
        await Steps.name_surname_edit.set()

    if callback.data == 'phone':
        await bot.send_message(callback.from_user.id, "Введіть новий номер телефону")
        await Steps.phone_number_edit.set()

    if callback.data == 'email':
        await bot.send_message(callback.from_user.id, "Введіть новий email")
        await Steps.get_email_edit.set()

    if callback.data == 'education':
        await bot.send_message(callback.from_user.id, "Напишіть рівень вашої освіти")
        await Steps.get_education_edit.set()

    if callback.data == 'soft_skills':
        await bot.send_message(callback.from_user.id, "Напишіть ваші Soft Skills")
        await Steps.get_soft_skills_edit.set()
    if callback.data == 'tech_skills':
        await bot.send_message(callback.from_user.id, "Напишіть ваші Tech Skills")
        await Steps.get_tech_skills_edit.set()
    if callback.data == 'projects':
        await bot.send_message(callback.from_user.id, "Додайте посилання на ваші проекти")
        await Steps.get_projects_edit.set()
    if callback.data == 'lang':
        await bot.send_message(callback.from_user.id, "Напишіть які ви знаєте мови та рівні мов")
        await Steps.get_lang.set()
    if callback.data == 'country':
        await bot.send_message(callback.from_user.id, "Напишіть з якої ви країни")
        await Steps.get_country_edit.set()
    if callback.data == 'city':
        await bot.send_message(callback.from_user.id, "Напишіть з якого ви міста")
        await Steps.get_city_edit.set()
    if callback.data == 'profession':
        await bot.send_message(callback.from_user.id, "Напишіть, що ви очікуєте від цієї посади(можете розповісти щось про себе")
        await Steps.get_profession_edit.set()
    if callback.data == 'description':
        await bot.send_message(callback.from_user.id, "Напишіть про ваш минулий досвід роботи(назва посади)")
        await Steps.get_description_edit.set()


@dp.message_handler(state=Steps.name_surname_edit)
async def edit_name_surname(message: types.Message):
    try:
        await db_executions.add_name_surname(message.from_user.id, message.text)
        await bot.send_message(message.from_user.id, 'Ваші дані оновлено')
        await bot.send_message(message.from_user.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.from_user.id, 'Виникла помилка')


@dp.message_handler(state=Steps.phone_number_edit)
async def edit_phone(message: types.Message):
    try:
        await db_executions.add_phone_number(message.from_user.id, message.text)
        await bot.send_message(message.from_user.id, 'Ваші дані оновлено')
        await bot.send_message(message.from_user.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.from_user.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_email_edit)
async def edit_email(message: types.Message):
    try:
        await db_executions.add_email(message.from_user.id, message.text)
        await bot.send_message(message.from_user.id, 'Ваші дані оновлено')
        await bot.send_message(message.from_user.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.from_user.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_education_edit)
async def edit_education(message: types.Message):
    try:
        await db_executions.add_education(message.from_user.id, message.text)
        await bot.send_message(message.from_user.id, 'Ваші дані оновлено')
        await bot.send_message(message.from_user.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.from_user.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_soft_skills_edit)
async def edit_soft_skills(message: types.Message):
    try:
        await db_executions.add_soft_skills(message.from_user.id, message.text)
        await bot.send_message(message.from_user.id, 'Ваші дані оновлено')
        await bot.send_message(message.from_user.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.from_user.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_tech_skills_edit)
async def edit_tech_skills(message: types.Message):
    try:
        await db_executions.add_tech_skills(message.from_user.id, message.text)
        await bot.send_message(message.from_user.id, 'Ваші дані оновлено')
        await bot.send_message(message.from_user.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.from_user.id, 'Виникла помилка')


@dp.message_handler(state=get_projects)
async def edit_projects(message: types.Message):
    try:
        await db_executions.add_projects(message.from_user.id, message.text)
        await bot.send_message(message.from_user.id, 'Ваші дані оновлено')
        await bot.send_message(message.from_user.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.from_user.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_lang_edit)
async def edit_lang(message: types.Message):
    try:
        if message.text.lower() == 'stop':
            await bot.send_message(message.from_user.id, 'Ваші дані оновлено')
            await bot.send_message(message.from_user.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
        else:
            await db_executions.clear_row(message.chat.id, 'lang')
            await db_executions.add_lang(message.from_user.id, message.text)
            await Steps.get_lang_level.set()
            await bot.send_message(message.from_user.id, 'Напишіть рівень мови🔴', reply_markup=lists)
    except:
        await bot.send_message(message.from_user.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_lang_level)
async def edit_lang_level(message: types.Message):
    try:
        if message.text.lower() == 'stop':
            await bot.send_message(message.from_user.id, 'Ваші дані оновлено')
            await bot.send_message(message.from_user.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
        else:
            await db_executions.clear_row(message.chat.id, 'lang_level')
            await db_executions.add_lang_level(message.from_user.id, message.text)
            await Steps.get_lang.set()
            await bot.send_message(message.from_user.id, 'Напишіть яку ви знаєте мову')
    except:
        await bot.send_message(message.from_user.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_country_edit)
async def edit_country(message: types.Message):
    try:
        await db_executions.add_country(message.from_user.id, message.text)
        await bot.send_message(message.from_user.id, 'Ваші дані оновлено')
        await bot.send_message(message.from_user.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.from_user.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_profession_edit)
async def edit_profession(message: types.Message):
    try:
        await db_executions.add_profession(message.from_user.id, message.text)
        await bot.send_message(message.from_user.id, 'Ваші дані оновлено')
        await bot.send_message(message.from_user.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.from_user.id, 'Виникла помилка')

@dp.message_handler(state=Steps.get_description_edit)
async def edit_description(message: types.Message):
    try:
        await db_executions.add_description(message.from_user.id, message.text)
        await Steps.get_work_experience.set()
        await message.answer('Напишіть про ваш минулий досвід роботи(назва посади)')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_work_experience_edit)
async def edit_work_experience(message: types.Message):
    try:
        if message.text.lower() == 'stop':
            await bot.send_message(message.from_user.id, 'Ваші дані оновлено')
            await bot.send_message(message.from_user.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
        else:
            await db_executions.clear_row(message.chat.id, 'work_experience')
            await db_executions.add_past_work(message.from_user.id, message.text)
            print('get_work_experience {}'.format(get_work_experience))
            await Steps.get_job_description_edit.set()
            await message.answer('Опишіть, що робили на цій роботі🔴', reply_markup=lists)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_job_description_edit)
async def edit_job_description(message: types.Message):
    try:
        if message.text.lower() == 'stop':
            await bot.send_message(message.from_user.id, 'Ваші дані оновлено')
            await bot.send_message(message.from_user.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
        else:
            await db_executions.clear_row(message.chat.id, 'job_description')
            await db_executions.add_job_description(message.from_user.id, message.text)
            print('get_job_description {}'.format(get_job_description))
            await Steps.get_how_long_edit.set()
            await message.answer('Скільки часу ви займали цю посаду?🔴', reply_markup=lists)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_how_long_edit)
async def edit_how_long(message: types.Message):
    try:
        if message.text.lower() == 'stop':
            await bot.send_message(message.from_user.id, 'Ваші дані оновлено')
            await bot.send_message(message.from_user.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
        else:
            await db_executions.clear_row(message.chat.id, 'how_long')
            await db_executions.add_how_long(message.from_user.id, message.text)
            print('get_how_long {}'.format(get_how_long))
            await Steps.get_work_experience_edit.set()
            await message.answer('Напишіть про ваш минулий досвід роботи(назва посади)🔴', reply_markup=lists)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')



async def on_startup(dp):
    await notify_admins(dp)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
