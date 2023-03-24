import telebot
from telebot.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
import random
import string
from app.main_db import writeTable
from config import *

bot = telebot.TeleBot(Token)

profession = ' '
name_surname = ' '
phone_number = ' '
email = ' '
education = list()
tech_skills = list()
soft_skills = list()
projects = list()
lang = list()
lang_level = list()
country = ' '
city = ' '
work_experience = list()
user_id = ' '
rand_password = ' '
description = ' '
how_long = list()
job_description = list()
update = False
next_step = False


def but_create():
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = KeyboardButton('📄Створити резюме📄')
    reply_markup.add(but1)
    return reply_markup


def generate_password():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(8))


@bot.message_handler(commands=['start'])
def start(message):
    global user_id
    user_id = message.chat.id
    bot.send_message(message.chat.id, '👋Привіт,{}!👋\n'
                                      '😃Це бот для створення резюме, думаю тобі сподобається😃'.format(message.from_user.first_name), reply_markup=but_create())
    print(user_id, message)


@bot.message_handler(content_types=['text'])
def message_reply(message):
    global user_id
    user_id = message.chat.id
    if message.text == '📄Створити резюме📄':
        reply_markup1 = ReplyKeyboardMarkup(resize_keyboard=True)
        msg = bot.send_message(message.chat.id, 'Напишіть ваше ім’я і прізвище', reply_markup=reply_markup1)
        bot.register_next_step_handler(msg, get_name_surname)


def get_name_surname(message):
    global name_surname, update
    if not update:
        if message.text == '-':
            pass
        elif message.text == '/start':
            start(message)
        else:
            name_surname = message.text
        msg = bot.send_message(message.chat.id, 'Напишіть ваш номер телефону')
        bot.register_next_step_handler(msg, get_phone_number)
    elif update:
        if message.text == '-':
            pass
        elif message.text == '/start':
            start(message)
        else:
            name_surname = message.text
            bot.send_message(message.chat.id, 'Хочете ще щось змінити?', reply_markup=end_keyboard())
            update = False
    print('name_surname =', name_surname)


def get_phone_number(message):
    global phone_number, update
    if not update:
        if message.text == '-':
            pass
        elif message.text == '/start':
            start(message)
        else:
            phone_number = message.text
        msg = bot.send_message(message.chat.id, 'Напишіть ваш email')
        bot.register_next_step_handler(msg, get_email)
    elif update:
        if message.text == '-':
            pass
        elif message.text == '/start':
            start(message)
        else:
            phone_number = message.text
            bot.send_message(message.chat.id, 'Хочете ще щось змінити?', reply_markup=end_keyboard())
            update = False
    print('phone number = ', phone_number)


def get_email(message):
    global email, update
    if not update:
        if message.text == '-':
            pass
        elif message.text == '/start':
            start(message)
        else:
            email = message.text
        msg = bot.send_message(message.chat.id, 'Напишіть рівень вашої освіти', reply_markup=next_step_but())
        bot.register_next_step_handler(msg, get_education)
    elif update:
        if message.text == '-':
            pass
        elif message.text == '/start':
            start(message)
        else:
            email = message.text
            bot.send_message(message.chat.id, 'Хочете ще щось змінити?', reply_markup=end_keyboard())
            update = False
    print('email = ', email)


def get_education(message):
    global education, update, next_step
    next_step = False
    if not next_step:
        if not update:
            if message.text == '-':
                pass
            elif message.text == '/start':
                start(message)
            else:
                education.append(message.text)
            bot.register_next_step_handler(bot.send_message(message.chat.id, 'Введіть наступний пункт'), get_education)
        elif update:
            if message.text == '-':
                pass
            elif message.text == '/start':
                start(message)
            else:
                education = message.text
                bot.send_message(message.chat.id, 'Хочете ще щось змінити?', reply_markup=end_keyboard())
                update = False

    print('education =', education)


def get_tech_skills(message):
    global tech_skills, update, next_step
    next_step = False
    if not next_step:
        if not update:
            if message.text == '-':
                pass
            elif message.text == '/start':
                start(message)
            else:
                tech_skills.append(message.text)
            bot.register_next_step_handler(bot.send_message(message.chat.id, 'Введіть наступний пункт'), get_tech_skills)
        elif update:
            if message.text == '-':
                pass
            elif message.text == '/start':
                start(message)
            else:

                tech_skills.append(message.text)
                bot.register_next_step_handler(
                    bot.send_message(message.chat.id, 'Введіть наступний пункт', reply_markup=markup45()), get_tech_skills)
                update = False

    print('tech skills = ', tech_skills)


def get_soft_skills(message):
    global soft_skills, update, next_step
    next_step = False
    if not next_step:
        if not update:
            if message.text == '-':
                pass
            elif message.text == '/start':
                start(message)
            else:
                soft_skills.append(message.text)
            bot.register_next_step_handler(bot.send_message(message.chat.id, 'Введіть наступний пункт'), get_soft_skills)
        elif update:
            if message.text == '-':
                pass
            elif message.text == '/start':
                start(message)
            else:
                soft_skills.append(message.text)
                bot.register_next_step_handler(
                    bot.send_message(message.chat.id, 'Введіть наступний пункт', reply_markup=markup45()), get_soft_skills)
                update = False

    print('soft_skills = ', soft_skills)


def get_projects(message):
    global projects, update, next_step
    next_step = False
    if not next_step:
        if not update:
            if message.text == '-':
                pass
            elif message.text == '/start':
                start(message)
            else:
                projects.append(message.text)
            bot.register_next_step_handler(bot.send_message(message.chat.id, 'Введіть наступний пункт'), get_projects)
        elif update:
            if message.text == '-':
                pass
            elif message.text == '/start':
                start(message)
            else:
                projects = message.text
                bot.send_message(message.chat.id, 'Хочете ще щось змінити?', reply_markup=end_keyboard())
                update = False
    print('projects = ', projects)


def get_lang(message):
    global lang, update, next_step
    next_step = False
    if not next_step:
        if not update:
            if message.text == '-':
                pass
            elif message.text == '/start':
                start(message)
            else:
                lang.append(message.text)
            msg = bot.send_message(message.chat.id, 'Введіть рівень знання цієї мови')
            bot.register_next_step_handler(msg, get_lang_level)
        elif update:
            if message.text == '-':
                pass
            elif message.text == '/start':
                start(message)
            else:
                lang.append(message.text)
                msg = bot.send_message(message.chat.id, 'Введіть рівень знання цієї мови')
                bot.register_next_step_handler(msg, get_lang_level)
    print('lang = ', lang)


def markup45():
    but = InlineKeyboardMarkup(row_width=1)
    but1 = InlineKeyboardButton('Закінчити редагування', callback_data='100')
    but.add(but1)
    return but


def get_lang_level(message):
    global lang_level, update, next_step
    next_step = False
    if not next_step:
        if not update:
            if message.text == '-':
                pass
            elif message.text == '/start':
                start(message)
            else:
                lang_level.append(message.text)
            bot.register_next_step_handler(bot.send_message(message.chat.id, 'Введіть наступну мову, якою ви володієте', reply_markup=next_step_but6()), get_lang)
        elif update:
            if message.text == '-':
                pass
            elif message.text == '/start':
                start(message)
            else:
                lang_level.append(message.text)
                bot.register_next_step_handler(
                    bot.send_message(message.chat.id, 'Введіть наступну мову, якою ви володієте',
                                     reply_markup=markup45()), get_lang)
                # bot.send_message(message.chat.id, 'Хочете ще щось змінити?', reply_markup=end_keyboard())
                # update = False
    print('lang_level = ', lang_level)


def get_country(message):
    global country, update
    if not update:
        if message.text == '-':
            pass
        elif message.text == '/start':
            start(message)
        else:
            country = message.text
        msg = bot.send_message(message.chat.id, 'Напишіть в якому місті ви живете')
        bot.register_next_step_handler(msg, get_city)
    elif update:
        if message.text == '-':
            pass
        elif message.text == '/start':
            start(message)
        else:
            country = message.text
            bot.send_message(message.chat.id, 'Хочете ще щось змінити?', reply_markup=end_keyboard())
            update = False
    print('country =', country)


def get_city(message):
    global city, update
    if not update:
        if message.text == '-':
            pass
        elif message.text == '/start':
            start(message)
        else:
            city = message.text
        msg = bot.send_message(message.chat.id, 'Напишіть на яку посаду претендуєте')
        bot.register_next_step_handler(msg, get_profession)
    elif update:
        if message.text == '-':
            pass
        elif message.text == '/start':
            start(message)
        else:
            city = message.text
            bot.send_message(message.chat.id, 'Хочете ще щось змінити?', reply_markup=end_keyboard())
            update = False
    print('city =', city)


def get_profession(message):
    global profession, update
    if not update:
        if message.text == '-':
            pass
        elif message.text == '/start':
            start(message)
        else:
            profession = message.text
        msg = bot.send_message(message.chat.id, 'Напишіть, що ви очікуєте від цієї посади(можете розповісти щось про себе)')
        bot.register_next_step_handler(msg, get_description)
    elif update:
        if message.text == '-':
            pass
        elif message.text == '/start':
            start(message)
        else:
            profession = message.text
            bot.send_message(message.chat.id, 'Хочете ще щось змінити?', reply_markup=end_keyboard())
            update = False
    print('profession =', profession)


def get_description(message):
    global description, update
    if not update:
        if message.text == '-':
            pass
        elif message.text == '/start':
            start(message)
        else:
            description = message.text
        msg = bot.send_message(message.chat.id, 'Напишіть про ваш минулий досвід роботи(назва посади)', reply_markup=next_step_but7())
        bot.register_next_step_handler(msg, get_work_experience)
    elif update:
        if message.text == '-':
            pass
        elif message.text == '/start':
            start(message)
        else:
            description = message.text
            bot.send_message(message.chat.id, 'Хочете ще щось змінити?', reply_markup=end_keyboard())
            update = False

    print('description =', description)


def get_work_experience(message):
    global work_experience, update, next_step
    next_step = False
    if not next_step:
        if not update:
            if message.text == '-':
                pass
            elif message.text == '/start':
                start(message)
            else:
                work_experience.append(message.text)
            msg = bot.send_message(message.chat.id, 'Опишіть, що робили на цій роботі')
            bot.register_next_step_handler(msg, get_job_description)
        elif update:
            if message.text == '-':
                pass
            elif message.text == '/start':
                start(message)
            else:
                work_experience.clear()
                work_experience.append(message.text)
                msg = bot.send_message(message.chat.id, 'Опишіть, що робили на цій роботі', reply_markup=markup45())
                bot.register_next_step_handler(msg, get_job_description)
    print('work_experience =', work_experience)


def get_job_description(message):
    global job_description, update, next_step
    next_step = False
    if not next_step:
        if not update:
            if message.text == '-':
                pass
            elif message.text == '/start':
                start(message)
            else:
                job_description.append(message.text)
            bot.register_next_step_handler(bot.send_message(message.chat.id, 'Скільки часу ви займали цю посаду?'), get_how_long)
        elif update:
            if message.text == '-':
                pass
            elif message.text == '/start':
                start(message)
            else:
                job_description = message.text
                bot.send_message(message.chat.id, 'Хочете ще щось змінити?', reply_markup=end_keyboard())
                update = False

    print('job_description =', job_description)


def get_how_long(message):
    global how_long, update, next_step
    if not next_step:
        if not update:
            if message.text == '-':
                pass
            elif message.text == '/start':
                start(message)
            else:
                how_long.append(message.text)
            msg = bot.send_message(message.chat.id, 'Напишіть наступний пункт')
            bot.register_next_step_handler(msg, get_work_experience)
        elif update:
            if message.text == '-':
                pass
            elif message.text == '/start':
                start(message)
            else:
                how_long = message.text
                bot.send_message(message.chat.id, 'Хочете ще щось змінити?', reply_markup=end_keyboard())
                update = False
    print('how_long =', how_long)


def next_step_but():
    markup = InlineKeyboardMarkup(row_width=1)
    but = InlineKeyboardButton('Продовжити складання резюме', callback_data='20')
    markup.add(but)
    return markup


def next_step_but2():
    markup = InlineKeyboardMarkup(row_width=1)
    but = InlineKeyboardButton('Продовжити складання резюме', callback_data='21')
    markup.add(but)
    return markup


def next_step_but3():
    markup = InlineKeyboardMarkup(row_width=1)
    but = InlineKeyboardButton('Продовжити складання резюме', callback_data='22')
    markup.add(but)
    return markup


def next_step_but4():
    markup = InlineKeyboardMarkup(row_width=1)
    but = InlineKeyboardButton('Продовжити складання резюме', callback_data='23')
    markup.add(but)
    return markup


def next_step_but6():
    markup = InlineKeyboardMarkup(row_width=1)
    but = InlineKeyboardButton('Продовжити складання резюме', callback_data='25')
    markup.add(but)
    return markup


def next_step_but7():
    markup = InlineKeyboardMarkup(row_width=1)
    but = InlineKeyboardButton('Продовжити складання резюме', callback_data='26')
    markup.add(but)
    return markup


def next_step_but8():
    markup = InlineKeyboardMarkup(row_width=1)
    but = InlineKeyboardButton('Продовжити складання резюме', callback_data='27')
    markup.add(but)
    return markup


def end_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    but1 = InlineKeyboardButton('Так', callback_data='15')
    but2 = InlineKeyboardButton('Ні', callback_data='16')
    markup.add(but1, but2)
    return markup


def changes():
    markup = InlineKeyboardMarkup(row_width=1)
    but1 = InlineKeyboardButton("😃Ім'я та прізвище😃", callback_data='1')
    but2 = InlineKeyboardButton("☎Номер телефону☎️", callback_data='2')
    but3 = InlineKeyboardButton("📧Email📧", callback_data='3')
    but4 = InlineKeyboardButton("🧐Освіта🧐", callback_data='4')
    but5 = InlineKeyboardButton("😄Soft Навички😄", callback_data='5')
    but14 = InlineKeyboardButton("😄Tech Навички😄", callback_data='14')
    but6 = InlineKeyboardButton("😲Проекти😲", callback_data='6')
    but7 = InlineKeyboardButton("✌Мови✌️", callback_data='7')
    but8 = InlineKeyboardButton("🗣Рівень мови🗣", callback_data='8')
    but9 = InlineKeyboardButton("👍Країна👍", callback_data='9')
    but10 = InlineKeyboardButton("🤟Місто🤟", callback_data='10')
    but11 = InlineKeyboardButton("👨‍🎓Професія👨‍🎓", callback_data='11')
    but12 = InlineKeyboardButton("😱Очікування😱", callback_data='12')
    but13 = InlineKeyboardButton("🤯Минула посада🤯", callback_data='13')
    but17 = InlineKeyboardButton("😱Ваша робота на минулій посаді😱", callback_data='17')
    but18 = InlineKeyboardButton("🤯Термін вашої минулої роботи🤯", callback_data='18')
    markup.add(but1, but2, but3, but4, but5, but6, but7, but8, but9, but10, but11, but12, but13, but14, but17, but18)
    return markup


@bot.callback_query_handler(func=lambda c: True)
def go_changes(call):
    global update, rand_password, next_step, name_surname, phone_number, email, education, lang, lang_level, country, city, rand_password,description, profession, soft_skills, tech_skills, projects, how_long, job_description, work_experience
    if call.data == '15':
        bot.send_message(call.from_user.id, 'Що бажаєте змінити?', reply_markup=changes())
    if call.data == '16':
        update = False
        rand_password = generate_password()
        writeTable(user_id, name_surname, phone_number, email, education, lang, lang_level, country, city, rand_password,
                description, profession, soft_skills, tech_skills, projects, how_long, job_description, work_experience)
        bot.send_message(call.from_user.id, f"🥳Ваше резюме готове🥳\n"
                                            f"🥸Ось ваші дані для реєстрації на сайті:🥸\n"
                                            f"🤐Telegram ID: {user_id}🤐\n"
                                            f"🤐Ваш пароль: {rand_password}🤐")
    elif call.data == '1':
        update = True
        msg = bot.send_message(call.from_user.id, 'Напишіть ваше ім’я і прізвище')
        bot.register_next_step_handler(msg, get_name_surname)
    if call.data == '2':
        update = True
        msg = bot.send_message(call.from_user.id, 'Напишіть ваш номер телефону')
        bot.register_next_step_handler(msg, get_phone_number)
    elif call.data == '3':
        update = True
        msg = bot.send_message(call.from_user.id, 'Напишіть ваш email')
        bot.register_next_step_handler(msg, get_email)
    if call.data == '4':
        update = True
        education.clear()
        msg = bot.send_message(call.from_user.id, 'Напишіть рівень вашої освіту')
        bot.register_next_step_handler(msg, get_education)
    elif call.data == '5':
        update = True
        soft_skills.clear()
        msg = bot.send_message(call.from_user.id, 'Напишіть про ваші Soft навички')
        bot.register_next_step_handler(msg, get_soft_skills)
    if call.data == '6':
        update = True
        projects.clear()
        msg = bot.send_message(call.from_user.id, 'Напишіть про ваші проекти або вставте посилання на них')
        bot.register_next_step_handler(msg, get_projects)
    elif call.data == '7':
        update = True
        msg = bot.send_message(call.from_user.id, 'Напишіть якими мовами ви володієте')
        bot.register_next_step_handler(msg, get_lang)
    if call.data == '8':
        update = True
        msg = bot.send_message(call.from_user.id, 'Напишіть рівень знання цих мов')
        bot.register_next_step_handler(msg, get_lang_level)
    elif call.data == '9':
        update = True
        msg = bot.send_message(call.from_user.id, 'Напишіть в якій країні ви живете')
        bot.register_next_step_handler(msg, get_country)
    if call.data == '10':
        update = True
        msg = bot.send_message(call.from_user.id, 'Напишіть в якому місті ви живете')
        bot.register_next_step_handler(msg, get_city)
    elif call.data == '11':
        update = True
        msg = bot.send_message(call.from_user.id, 'Напишіть на яку посаду претендуєте')
        bot.register_next_step_handler(msg, get_profession)
    if call.data == '12':
        update = True
        msg = bot.send_message(call.from_user.id, 'Напишіть ваші очікування від цієї посади')
        bot.register_next_step_handler(msg, get_description)
    elif call.data == '13':
        update = True
        work_experience.clear()
        msg = bot.send_message(call.from_user.id, 'Напишіть про ваш минулий досвід роботи(назва посади)')
        bot.register_next_step_handler(msg, get_work_experience)
    if call.data == '14':
        update = True
        tech_skills.clear()
        msg = bot.send_message(call.from_user.id, 'Напишіть про ваші Tech навички')
        bot.register_next_step_handler(msg, get_tech_skills)
    elif call.data == '17':
        update = True
        msg = bot.send_message(call.from_user.id, 'Що ви робили на цій посаді(опишіть)')
        bot.register_next_step_handler(msg, get_job_description)
    if call.data == '18':
        update = True
        how_long.clear()
        msg = bot.send_message(call.from_user.id, 'Скільки часу ви займали цю посаду?')
        bot.register_next_step_handler(msg, get_how_long)
    elif call.data == '20':
        next_step = True
        msg = bot.send_message(call.from_user.id, 'Напишіть ваші Tech Skills', reply_markup=next_step_but2())
        bot.clear_step_handler(msg)
        bot.register_next_step_handler(msg, get_tech_skills)
    if call.data == '21':
        next_step = True
        msg = bot.send_message(call.from_user.id, 'Напишіть ваші Soft Skills', reply_markup=next_step_but3())
        bot.clear_step_handler(msg)
        bot.register_next_step_handler(msg, get_soft_skills)
    elif call.data == '22':
        next_step = True
        msg = bot.send_message(call.from_user.id, 'Вставте посилання на ваші проекти', reply_markup=next_step_but4())
        bot.clear_step_handler(msg)
        bot.register_next_step_handler(msg, get_projects)
    if call.data == '23':
        next_step = True
        msg = bot.send_message(call.from_user.id, 'Напишіть якими мовами ви володієте', reply_markup=next_step_but6())
        bot.clear_step_handler(msg)
        bot.register_next_step_handler(msg, get_lang)
    elif call.data == '26':
        next_step = True
        msg = bot.send_message(call.from_user.id, "😎Ваше резюме готове, перевірте свої дані:😎\n"
                                          f"Ім'я та прізивще: {name_surname}\n"
                                          f"Номер телефону: {phone_number}\n"
                                          f"Електронна пошта: {email}\n"
                                          f"Освіта: {education}\n"
                                          f"Tech Навички: {tech_skills}\n"
                                          f"Soft Навички: {soft_skills}\n"
                                          f"Посилання на ваші проекти: {projects}\n"
                                          f"Мови: {lang}\n"
                                          f"Рівень знання цих мов: {lang_level}\n"
                                          f"Ваша країна: {country}\n"
                                          f"Ваше місто: {city}\n"
                                          f"Посада на яку претендуєте: {profession}\n"
                                          f"Ваші очікування від роботи: {description}\n"
                                          f"Ваш минулий досвід роботи(минула посада): {work_experience}\n"
                                          f"Що ви робили на цій посаді: {job_description}\n"
                                          f"Скільки часу ви займали цю посаду: {how_long}\n"
                                          "Чи хочете відредагувати свої дані?'\n", reply_markup=end_keyboard())
        bot.clear_step_handler(msg)


    if call.data == '25':
        next_step = True
        msg = bot.send_message(call.from_user.id, 'Напишіть з якої ви країни')
        bot.clear_step_handler(msg)
        bot.register_next_step_handler(msg, get_country)
    elif call.data == '100':
        next_step = True
        update = False
        bot.send_message(call.from_user.id, 'Бажаєте ще щось змінити ?', reply_markup=end_keyboard())


bot.polling(none_stop=True)
