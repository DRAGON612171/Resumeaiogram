# from aiogram import types, Dispatcher, Bot
# from steps import *
from keyboards import *
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from Resumeaiogram import config
# from aiogram.utils import executor, callback_data
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from Resumeaiogram.app.database import db_executions
# from Resumeaiogram import config
# from bot_aiogram import get_lang, get_lang_level, get_work_experience, get_job_description, get_how_long
#
# bot = Bot(token=config.Token)
# dp = Dispatcher(bot, storage=MemoryStorage())
#
#
# @dp.message_handler(state=Steps.get_lang)
# async def get_lang(message: types.Message):
#     get_lang = message.text
#     print('lang {}'.format(get_lang))
#     await Steps.get_lang_level.set()
#     await message.answer('Напишіть рівень знання цих мов')
#
#
# @dp.message_handler(state=Steps.get_lang_level)
# async def get_lang_level(message: types.Message):
#     get_lang_level = message.text
#     print('lang_level {}'.format(get_lang_level))
#
#
#
# def cycle_lang(message: types.Message):
#     bot.send_message('Ввести ще одну мову')
#     end_keyboard()
#     if callback_data == 15:
#         Steps.get_lang.set()
#         message.answer('Напишіть рівень знання цих мов')
#     elif callback_data == 16:
#         Steps.get_country.set()
#         message.answer('Напишіть з якої ви країни')
#
#
# async def skip_three_functions(message: types.Message, state: FSMContext):
#     await get_work_experience(message, state)
#     await get_job_description(message, state)
#     await get_how_long(message, state)


but_skip = ReplyKeyboardMarkup(
    keyboard=[
        [
          KeyboardButton(text='Немає досвіду роботи')
        ]
    ],
    resize_keyboard=True
)

# создаем кнопку "Skip 3 functions"
# skip_button = KeyboardButton(text="Немає досвіду роботи")
#
# # создаем клавиатуру с кнопкой "Skip 3 functions"
# keyboard_skip = ReplyKeyboardMarkup(resize_keyboard=True)
# keyboard_skip.add(skip_button)

# отправляем сообщение с клавиатурой
# await message.answer("Нажмите кнопку, чтобы пропустить три функции", reply_markup=keyboard)

# задаем обработчик нажатия на кнопку
# dp.register_message_handler(skip_three_functions, lambda message: message.text == "Немає досвіду роботи")
# #
# if message.text == '📄Створити резюме📄':
#     reply_markup1 = ReplyKeyboardMarkup(resize_keyboard=True)
#     await message.answer('Напишіть ваше ім’я і прізвище', reply_markup=reply_markup1)
#     await Steps.name_surname.set()
#
#
#
#
# @dp.message_handler(state=Steps.get_projects)
# async def get_soft_skills(message: types.Message):
#     get_projects = message.text
#     print('projects {}'.format(get_projects))
#     await Steps.get_lang_level.set()
#     await message.answer('Напишіть з які ви знаєте мову')
#
#
# lang = []
# lang_level = []
#
#
#
# @dp.message_handler(state=Steps.get_lang)
# async def get_lang(message: types.Message):
#     if message.text.lower() == 'stop':
#         await Steps.get_country.set()
#         await message.answer('Напишіть з якої ви країни')
#     else:
#         lang.append(message.text)
#         await Steps.get_lang_level.set()
#         await message.answer('Напишіть рівень знання цієї мови')
#         print('lang {}'.format(lang))
#
# @dp.message_handler(state=Steps.get_lang_level)
# async def get_lang_level(message: types.Message):
#     if message.text.lower() == 'stop':
#         await Steps.get_country.set()
#         await message.answer('Напишіть з якої ви країни')
#     else:
#         lang_level.append(message.text)
#         await Steps.get_lang.set()
#         await message.answer('Напишіть наступну мову або натисніть stop', reply_markup=lists)
#         print('lang_level {}'.format(lang_level))
# @dp.message_handler(state=Steps.get_country)
