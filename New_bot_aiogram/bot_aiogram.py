import random
import string
from io import BytesIO
from PIL import Image
from aiogram import types, Dispatcher, Bot
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Resumeaiogram import config
from admins_notify import notify_admins
from Resumeaiogram.database.SQLAlchemy_connection import session, ResumeBot
from steps import Steps
from keyboards import but_create, end_keyboard, changes, lists, confirm, work_pass, image
from aiogram.dispatcher import FSMContext

bot = Bot(token=config.Token)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['instruction'], state='*')
async def instruction(message: types.Message,state: FSMContext):
    await bot.send_message(message.chat.id, 'Тут все просто) \n'
                                            'Всі данні слід записувати через кому, а коли побачите "🔴",'
                                            'то треба вводити свої данні по одному, тобто один пункт'
                                            ' в одному повідомленні.\n'
                                            'Пропонуємо спочатку передивитися приклад заповнення: /example')
    await state.finish()


@dp.message_handler(commands=['example'], state='*')
async def example(message: types.Message,state: FSMContext):
    photo = open('resume_example.jpg', 'rb')
    await bot.send_message(message.chat.id, 'Ось приклад заповнення резюме:')
    await bot.send_photo(message.chat.id, photo=photo)
    await state.finish()


@dp.message_handler(commands=['clear'], state='*')
async def clear(message: types.Message,state: FSMContext):
    await bot.send_message(message.chat.id, 'Ви впевнені, що хочете видалити всі данні?', reply_markup=confirm)
    await state.finish()


@dp.message_handler(commands=['website'], state='*')
async def website(message: types.Message,state: FSMContext):
    resumes = session.query(ResumeBot).filter_by(id=message.chat.id).all()
    for resume in resumes:
        await bot.send_message(message.chat.id, f"Ваші дані для входу:\n"
                                                f"ID = {resume.id}\n"
                                                f"PASSWORD = {resume.password}")
    await state.finish()


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, '👋Привіт, {}!👋\n'
                                            '😃Це бот для створення резюме, думаю тобі сподобається😃 \n'
                                            'Якщо ви вперше складаєте резюме, то ознайомтеся як це краще зробити: \n'
                                            '/instruction \n'
                                            '/example\n'
                                            'Якщо бажаєте видалити минулі дані, то використайте команду /clear'.format
    (message.from_user.first_name), reply_markup=but_create)
    existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
    await state.finish()
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
        await message.answer('Напишіть ваше ім’я і прізвище', reply_markup=types.ReplyKeyboardRemove())
        # PASSWORD
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(8))
        try:
            existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
            existing_user.update_info(password=password)
            session.commit()
            await Steps.name_surname.set()
        except :
            await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(content_types=['text'], state=Steps.name_surname)
async def name_surname(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(name_surname=message.text)
        session.commit()
        print('name_surname {}'.format(message.text))
        await Steps.get_image.set()
        await message.answer('Прикріпіть своє фото', reply_markup=image)
    except :
        await message.answer('Виникла помилка')


@dp.message_handler(content_types=['photo', 'text'], state=Steps.get_image)
async def get_image(message: types.Message):
    try:
        if message.text == 'Не хочу додавати фото':
            await bot.send_message(message.chat.id, 'Напишіть ваш номер телефону')
            await Steps.phone_number.set()
        else:
            existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
            photo = message.photo[-1]
            file = await photo.get_file()

            # Преобразование изображения в байты
            image_bytes = BytesIO()
            await file.download(destination_file=image_bytes)
            image_bytes.seek(0)

            # Открытие изображения с использованием Pillow
            image = Image.open(image_bytes)

            # Преобразование изображения обратно в байты
            image_bytes = BytesIO()
            image.save(image_bytes, format='JPEG')
            image_bytes.seek(0)

            existing_user.update_info(image=image_bytes.read())
            session.commit()
            await bot.send_message(message.chat.id, 'Напишіть ваш номер телефону', reply_markup=types.ReplyKeyboardRemove())
            await Steps.phone_number.set()
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(content_types=['text'], state=Steps.phone_number)
async def phone_number(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(phone_number=message.text)
        session.commit()
        print('phone_number {}'.format(message.text))
        await Steps.get_email.set()
        await message.answer('Напишіть ваш email')
    except :
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
    except :
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
    except :
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
    except :
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
    except :
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
    except :
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_lang)
async def get_lang(message: types.Message):
    try:
        if message.text.lower() == 'stop':
            await Steps.get_country.set()
            await message.answer('Напишіть з якої ви країни')
        else:
            existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
            new = []
            if existing_user.lang:
                for i in existing_user.lang:
                    new.append(i)
            new.append(message.text)
            existing_user.update_info(lang=new)
            session.commit()
            print('lang{}'.format(message.text))
            await Steps.get_lang_level.set()
            await message.answer('Напишіть рівень мови🔴', reply_markup=types.ReplyKeyboardRemove())
    except :
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_lang_level)
async def get_lang_level(message: types.Message):
    try:
        if message.text.lower() == 'stop':
            await Steps.get_country.set()
            await message.answer('Напишіть з якої ви країни')
        else:
            existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
            new = []
            if existing_user.lang_level:
                for i in existing_user.lang_level:
                    new.append(i)
            new.append(message.text)
            existing_user.update_info(lang_level=new)
            session.commit()
            await Steps.get_lang.set()
            await message.answer('Напишіть яку ви знаєте мову', reply_markup=lists)
    except :
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_country)
async def get_country(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(country=message.text)
        session.commit()
        print('country {}'.format(message.text))
        await Steps.get_city.set()
        await message.answer('Напишіть з якого ви міста')
    except :
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
    except :
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
    except :
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_description)
async def get_description(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(description=message.text)
        session.commit()
        print('description {}'.format(message.text))
        await Steps.get_work_experience.set()
        await message.answer('Напишіть про ваш минулий досвід роботи(назва посади)🔴',reply_markup=work_pass)
    except :
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_work_experience)
async def get_work_experience(message: types.Message):
    existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
    new = []
    try:
        if message.text.lower() == 'stop' or message.text.lower() == 'немає досвіду роботи':
            await bot.send_message(message.chat.id, '😎Ваше резюме готове, перевірте свої дані:😎', reply_markup=types.ReplyKeyboardRemove())
            await end_message(message)
        else:
            if existing_user.past_work == None:
                new.append(message.text)
                existing_user.update_info(past_work=new)
                session.commit()
            else:
                for i in existing_user.past_work:
                    new.append(i)
                new.append(message.text)
                existing_user.update_info(past_work=new)
                session.commit()
            print('get_work_experience {}'.format(message.text))
            await Steps.get_job_description.set()
            await message.answer('Опишіть, що робили на цій роботі🔴', reply_markup=lists)
    except Exception as e:
        print(e)
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_job_description)
async def get_job_description(message: types.Message):
    existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
    new = []
    try:
        if message.text.lower() == 'stop' or message.text.lower() == 'Немає досвіду роботи':
            await bot.send_message(message.chat.id, '😎Ваше резюме готове, перевірте свої дані:😎')
            await end_message(message)
        else:
            if existing_user.job_description == None:
                new.append(message.text)
                existing_user.update_info(job_description=new)
                session.commit()
            else:
                for i in existing_user.job_description:
                    new.append(i)
                new.append(str(message.text))
                existing_user.update_info(job_description=new)
                session.commit()
            print('get_job_description {}'.format(message.text))
            await Steps.get_how_long.set()
            await message.answer('Скільки часу ви займали цю посаду?🔴', reply_markup=types.ReplyKeyboardRemove())
    except :
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.get_how_long)
async def get_how_long(message: types.Message):
    existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
    new = []
    try:
        if message.text.lower() == 'stop' or message.text.lower() == 'Немає досвіду роботи':
            await bot.send_message(message.chat.id, '😎Ваше резюме готове, перевірте свої дані:😎')
            await end_message(message)
        else:
            if existing_user.how_long == None:
                new.append(message.text)
                existing_user.update_info(how_long=new)
                session.commit()
            else:
                for i in existing_user.how_long:
                    new.append(i)
                new.append(str(message.text))
                existing_user.update_info(how_long=new)
                session.commit()
            print('get_how_long {}'.format(message.text))
            await Steps.get_work_experience.set()
            await message.answer('Напишіть про ваш минулий досвід роботи(назва посади)🔴')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


async def end_message(message):
    resumes = session.query(ResumeBot).filter_by(id=message.chat.id).all()
    for resume in resumes:
        await bot.send_message(message.chat.id, f"Ім'я та прізивще: {resume.name_surname}\n"
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
        resumes = session.query(ResumeBot).filter_by(id=callback.from_user.id).all()
        for resume in resumes:
            await bot.send_message(callback.from_user.id, f"Все готово, можете зайти до сайту і отримати своє резюме🥳\n"
                                                      "Ваші дані для входу:\n"
                                                      f"ID = {resume.id}\n"
                                                      f"PASSWORD = {resume.password}")
        await bot.send_message(callback.from_user.id, "http://goiteens2.pythonanywhere.com/")

    if callback.data == 'name_surname':
        await bot.send_message(callback.from_user.id, "Нове нове прізвище та ім'я")
        await Steps.name_surname_edit.set()

    elif callback.data == 'image':
        await bot.send_message(callback.from_user.id, "Відправляйте нову фотку")
        await Steps.image_edit.set()

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
        await bot.send_message(callback.from_user.id, "Напишіть які ви знаєте мови ")
        await Steps.lang_edit.set()
    if callback.data == 'lang_level':
        await bot.send_message(callback.from_user.id, "Напишіть рівні ваших мов")
        await Steps.lang_level_edit.set()
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
    if callback.data == 'work_experience':
        await bot.send_message(callback.from_user.id,"Напишіть про ваш минулий досвід роботи")
        await Steps.work_experience_edit.set()
    if callback.data == 'job_description':
        await bot.send_message(callback.from_user.id, "Напишіть, що ви робили на вашій минулій роботі")
        await Steps.job_description_edit.set()
    if callback.data == 'how_long':
        await bot.send_message(callback.from_user.id, "Напишіть скільки часу ви працювали на минулій роботі")
        await Steps.how_long_edit.set()
    if callback.data == 'confirm':
        try:
            session.query(ResumeBot).filter_by(id=callback.from_user.id).delete()
            session.commit()
            await bot.send_message(callback.from_user.id, 'Ваші данні видалено\n'
                                                          '/start')
        except :
            await bot.send_message(callback.from_user.id, 'Виникла помилка')
    if callback.data == 'cancel':
        await bot.send_message(callback.from_user.id, 'Операція скасована')


@dp.message_handler(state=Steps.name_surname_edit)
async def edit_name_surname(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(name_surname=message.text)
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except :
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(content_types=['photo'], state=Steps.image_edit)
async def image_edit(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        photo = message.photo[-1]
        file = await photo.get_file()

        # Преобразование изображения в байты
        image_bytes = BytesIO()
        await file.download(destination_file=image_bytes)
        image_bytes.seek(0)

        # Открытие изображения с использованием Pillow
        image = Image.open(image_bytes)

        # Преобразование изображения обратно в байты
        image_bytes = BytesIO()
        image.save(image_bytes, format='JPEG')
        image_bytes.seek(0)

        existing_user.update_info(image=image_bytes.read())
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.phone_number_edit)
async def edit_phone_number(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(phone_number=message.text)
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except :
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.email_edit)
async def edit_email(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(email=message.text)
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except :
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.education_edit)
async def edit_education(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(education=message.text.split(','))
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except :
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.soft_skills_edit)
async def edit_soft_skills(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(soft_skills=message.text.split(','))
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except :
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.tech_skills_edit)
async def edit_tech_skills(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(tech_skills=message.text.split(','))
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.projects_edit)
async def edit_projects(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(projects=message.text.split(','))
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.lang_edit)
async def edit_lang(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(lang=message.text.split(','))
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.lang_level_edit)
async def edit_lang_level(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(lang_level=message.text.split(','))
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.country_edit)
async def edit_country(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(country=message.text)
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.city_edit)
async def edit_city(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(city=message.text)
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.profession_edit)
async def edit_profession(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(profession=message.text)
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.description_edit)
async def edit_description(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(description=message.text)
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.work_experience_edit)
async def work_experience_edit(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(past_work=message.text.split(","))
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.job_description_edit)
async def edit_job_description(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(job_description=message.text.split(','))
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(state=Steps.how_long_edit)
async def edit_how_long(message: types.Message):
    try:
        existing_user = session.query(ResumeBot).filter_by(id=message.chat.id).first()
        existing_user.update_info(how_long=message.text.split(','))
        session.commit()
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
        await bot.send_message(message.chat.id, 'Бажаєте змінити ще щось?', reply_markup=end_keyboard)
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


async def on_startup(dp):
    await notify_admins(dp)

if __name__ == '__main__':
    executor.start_polling(dp)
