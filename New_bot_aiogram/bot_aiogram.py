import random
import string
from aiogram import types, Dispatcher, Bot

from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
# from Resumeaiogram import config
# from admins_notify import notify_admins
from database.SQLAlchemy_connection import session, ResumeBot
# from Resumeaiogram.database import SQLAlchemy_connection
# from Resumeaiogram.database.SQLAlchemy_connection import session, ResumeBot
from steps import *
from keyboards import *

bot = Bot(token="6149467271:AAF9A_Kl5L3lU8BcVjhfc3EP8tqrc-rv1Fs")
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
    await bot.send_message(message.chat.id, '👋Привіт!👋\n'  
                                            '😃Це бот для створення резюме, думаю тобі сподобається😃 \n'
                                            'Якщо ви вперше складаєте резюме, то ознайомтеся як це краще зробити: \n'
                                            '/instruction \n'
                                            '/example'.format(message.from_user.first_name), reply_markup=but_create)
    existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
    if existing_user:
        pass
    else:
        # Додати новий запис про користувача в базу даних
        new_user = ResumeBot(id=message.chat.id)
        session.add(new_user)
        session.commit()


@dp.message_handler(content_types=['text'])
async def create_resume(message: types.Message):
    if message.text == '📄Створити резюме📄':
        reply_markup1 = ReplyKeyboardMarkup(resize_keyboard=True)
        await message.answer('Напишіть ваше ім’я і прізвище', reply_markup=reply_markup1)
        # PASSWORD
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(8))
        try:
            existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
            existing_user.update_info(password=password)
            session.commit()
            await Steps.name_surname.set()
        except Exception as e:
            print(e)


@dp.message_handler(content_types=['text'], state=Steps.name_surname)
async def name_surname(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(name_surname=message.text)
        session.commit()
        print('name_surname {}'.format(message.text))
        await Steps.phone_number.set()
        await message.answer('Напишіть ваш номер телефону')
    except Exception as e:
        print(2, e)
        await message.answer('Виникла помилка')


@dp.message_handler(content_types=['text'], state=Steps.phone_number)
async def phone_number(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(phone_number=message.text)
        session.commit()
        print('phone_number {}'.format(message.text))
        await Steps.get_email.set()
        await message.answer('Напишіть ваш email')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_email)
async def get_email(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(email=message.text)
        session.commit()
        print('email {}'.format(get_email))
        await Steps.get_education.set()
        await message.answer('Напишіть рівень вашої освіти')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_education)
async def get_education(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(education=message.text.split(','))
        session.commit()
        print('get_education {}'.format(message.text))
        await message.answer('Напишіть ваші Tech Skills')
        await Steps.get_tech_skills.set()
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_tech_skills)
async def get_tech_skills(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(tech_skills=message.text.split(','))
        session.commit()
        print('tech skills {}'.format(message.text))
        await Steps.get_soft_skills.set()
        await message.answer('Напишіть ваші Soft Skills')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_soft_skills)
async def get_soft_skills(message: types.Message()):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(soft_skills=message.text.split(','))
        session.commit()
        print('soft skills {}'.format(message.text))
        await Steps.get_projects.set()
        await message.answer('Додайте посилання на ваші проекти')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_projects)
async def get_projects(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(projects=message.text.split(','))
        session.commit()
        print('projects {}'.format(message.text))
        await Steps.get_lang.set()
        await message.answer('Напишіть яку ви знаєте мову🔴')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_lang)
async def get_lang(message: types.Message):
    # try:
        if message.text.lower() == 'stop':
            await Steps.get_country.set()
            await message.answer('Напишіть з якої ви країни')
        else:
            existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
            existing_user.update_info(lang=message.text.split(','))
            session.commit()
            # existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
            # lang = message.text.split(',')
            # existing_user.add_lang(lang)
            # session.commit()
            print('lang{}'.format(message.text))
            await Steps.get_lang_level.set()
            await message.answer('Напишіть рівень мови🔴', reply_markup=lists)
    # except:
    #     await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_lang_level)
async def get_lang_level(message: types.Message):
    # try:
        if message.text.lower() == 'stop':
            await Steps.get_country.set()
            await message.answer('Напишіть з якої ви країни')
        else:
            existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
            existing_user.update_info(lang_level=message.text.split(','))
            session.commit()
            # existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
            # lang_level = message.text.split(',')
            # existing_user.add_lang_level(lang_level)
            # session.commit()
            await Steps.get_lang.set()
            await message.answer('Напишіть яку ви знаєте мову')
    # except:
    #     await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_country)
async def get_country(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(country=message.text)
        session.commit()
        print('country {}'.format(message.text))
        await Steps.get_city.set()
        await message.answer('Напишіть з якого ви міста')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_city)
async def get_city(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(city=message.text)
        session.commit()
        print('city {}'.format(message.text))
        await Steps.get_profession.set()
        await message.answer('Напишіть на яку посаду претендуєте')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_profession)
async def get_profession(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(profession=message.text)
        session.commit()
        print('profession {}'.format(message.text))
        await Steps.get_description.set()
        await message.answer('Напишіть, що ви очікуєте від цієї посади(можете розповісти щось про себе')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_description)
async def get_description(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(description=message.text)
        session.commit()
        print('description {}'.format(message.text))
        await Steps.get_work_experience.set()
        await message.answer('Напишіть про ваш минулий досвід роботи(назва посади)🔴')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')

@dp.message_handler(state=Steps.get_work_experience)
async def get_work_experience(message: types.Message):
    try:
        if message.text.lower() == 'stop':
            await Steps.end_message.set()
            await bot.send_message(message.chat.id,'😎Ваше резюме готове, перевірте свої дані:😎')
        else:
            # session.query(ResumeBot).filter_by(id=message.chat.id).update(
            #     {ResumeBot.past_work: ResumeBot.past_work + [message.text]},
            #     synchronize_session=False
            # )
            # session.commit()
            print('get_work_experience {}'.format(message.text))
            await Steps.get_job_description.set()
            await message.answer('Опишіть, що робили на цій роботі🔴', reply_markup=lists)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_job_description)
async def get_job_description(message: types.Message):
    try:
        if message.text.lower() == 'stop':
            await Steps.end_message.set()
            await bot.send_message(message.chat.id,'😎Ваше резюме майже готове, перевірте свої дані:😎')
        else:
            # session.query(ResumeBot).filter_by(id=message.chat.id).update(
            #     {ResumeBot.job_description: ResumeBot.job_description + [message.text]},
            #     synchronize_session=False
            # )
            session.commit()
            print('get_job_description {}'.format(message.text))
            await Steps.get_how_long.set()
            await message.answer('Скільки часу ви займали цю посаду?🔴', reply_markup=lists)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_how_long)
async def get_how_long(message: types.Message):
    try:
        if message.text.lower() == 'stop':
            await Steps.end_message.set()
            await bot.send_message(message.chat.id,'😎Ваше резюме готове, перевірте свої дані:😎')
        else:
            # session.query(ResumeBot).filter_by(id=message.chat.id).update(
            #     {ResumeBot.how_long: ResumeBot.how_long + [message.text]},
            #     synchronize_session=False
            # )
            # session.commit()
            print('get_how_long {}'.format(message.text))
            await Steps.get_work_experience.set()
            await message.answer('Напишіть про ваш минулий досвід роботи(назва посади)🔴', reply_markup=lists)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.end_message)
async def end_message(message: types.Message):
    resumes = session.query(ResumeBot).filter_by(id=message.chat.id).all()
    for resume in resumes:
        print(resume.id, resume.name_surname, resume.phone_number, resume.email, resume.education, resume.lang, resume.lang_level, resume.country, resume.city, resume.description, resume.work_experience, resume.profession, resume.soft_skills, resume.tech_skills, resume.projects, resume.how_long, resume.job_description, resume.past_work, resume.password)
    await bot.send_message(message.chat.id,f"Ім'я та прізивще: {resume.name_surname}\n"
                             f"Номер телефону: {resume.phone_number}\n"
                             f"Електронна пошта: {resume.email}\n"
                             f"Освіта: {resume.education}\n"
                             f"Tech Навички: {resume.tech_skills}\n"
                             f"Soft Навички: {resume.soft_skills}\n"
                             f"Посилання на ваші проекти: {resume.projects}\n"
                             f"Мови: {resume.lang}\n"
                             f"Рівень знання цих мов:{resume.lang_level}\n"
                             f"Ваша країна: {resume.country}\n"
                             f"Ваше місто: {resume.city}\n"
                             f"Посада на яку претендуєте: {resume.profession}\n"
                             f"Ваші очікування від роботи: {resume.description}\n"
                             f"Що ви робили на минулій посаді: {resume.past_work}\n"
                             f"Скільки часу ви займали цю посаду: {resume.how_long}\n"
                             "Чи хочете відредагувати свої дані?'\n", reply_markup=end_keyboard)


@dp.callback_query_handler(state='*')
async def bot_changes(callback: types.callback_query):
    if callback.data == '15':
        await bot.send_message(callback.from_user.id, "Що бажаєте змінити?", reply_markup=changes)
    elif callback.data == '16':
        resume = session.query(ResumeBot).filter_by(id=callback.from_user.id).all()
        await bot.send_message(callback.from_user.id, f"Все готово, можете зайти до сайту і отримати своє резюме🥳\n"
                                                  "Ваші дані для входу:\n"
                                                  f"ID = {resume.id}\n"
                                                  f"PASSWORD = {resume.password}")
        #Додати посилання на сайт
        await bot.send_message(callback.from_user.id, "http://goiteens2.pythonanywhere.com/")

    if callback.data == 'name_surname':
        await bot.send_message(callback.from_user.id, "Нове нове прізвище та ім'я")
        await Steps.name_surname_edit.set()

    if callback.data == 'phone':
        await bot.send_message(callback.from_user.id, "Введіть новий номер телефону")
        await Steps.phone_number_edit.set()

    if callback.data == 'email':
        await bot.send_message(callback.from_user.id, "Введіть новий email")
        await Steps.email_edit.set()

    if callback.data == 'education':
        await bot.send_message(callback.from_user.id, "Напишіть рівень вашої освіти")
        await Steps.education_edit.set()

    if callback.data == 'soft_skills':
        await bot.send_message(callback.from_user.id, "Напишіть ваші Soft Skills")
        await Steps.soft_skills_edit.set()
    if callback.data == 'tech_skills':
        await bot.send_message(callback.from_user.id, "Напишіть ваші Tech Skills")
        await Steps.tech_skills_edit.set()
    if callback.data == 'projects':
        await bot.send_message(callback.from_user.id, "Додайте посилання на ваші проекти")
        await Steps.projects_edit.set()
    if callback.data == 'lang':
        await bot.send_message(callback.from_user.id, "Напишіть які ви знаєте мови та рівні мов")
        await Steps.edit_langs.set()
    if callback.data == 'country':
        await bot.send_message(callback.from_user.id, "Напишіть з якої ви країни")
        await Steps.country_edit.set()
    if callback.data == 'city':
        await bot.send_message(callback.from_user.id, "Напишіть з якого ви міста")
        await Steps.city_edit.set()
    if callback.data == 'profession':
        await bot.send_message(callback.from_user.id, "Напишіть на яку посаду ви претендуєте")
        await Steps.profession_edit.set()
    if callback.data == 'description':
        await bot.send_message(callback.from_user.id, "Напишіть, що ви очікуєте від цієї посади(можете розповісти щось про себе")
        await Steps.description_edit.set()
    # if callback.data == 'past_work':
    #     await bot.send_message(callback.from_user.id, "Напишіть про ваш минулий досвід роботи(назва посади)")
    #     await Steps.edit_professions.set()
    if callback.data == 'confirm':
        try:
            session.query(ResumeBot).filter_by(id=callback.from_user.id).delete()
            session.commit()
            await bot.send_message(callback.from_user.id, 'Ваші данні видалено')
        except:
            await bot.send_message(callback.from_user.id, 'Виникла помилка')
    if callback.data == 'cancel':
        await bot.send_message(callback.from_user.id, 'Операція скасована')


@dp.message_handler(state=Steps.name_surname_edit)
async def edit_name_surname(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.name_surname = None
        existing_user.name_surname = message.text
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.phone_number_edit)
async def edit_phone_number(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.phone_number = message.text
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.email_edit)
async def edit_email(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.email = message.text
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.education_edit)
async def edit_education(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.education = message.text
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.soft_skills_edit)
async def edit_soft_skills(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.soft_skills = message.text
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.tech_skills_edit)
async def edit_tech_skills(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.tech_skills = message.text
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.projects_edit)
async def edit_projects(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.projects = message.text
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.lang_edit)
async def edit_lang(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.lang = message.text
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.lang_level_edit)
async def edit_lang_level(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.lang_level = message.text
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.country_edit)
async def edit_country(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.country = message.text
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.city_edit)
async def edit_city(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.city = message.text
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.profession_edit)
async def edit_profession(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.profession = message.text
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.description_edit)
async def edit_description(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.description = message.text
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.job_description_edit)
async def edit_job_description(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.job_description = message.text
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.job_description_edit)
async def edit_how_long(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.how_long = message.text
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


async def on_startup(dp):
    await notify_admins(dp)

if __name__ == '__main__':
    executor.start_polling(dp)
