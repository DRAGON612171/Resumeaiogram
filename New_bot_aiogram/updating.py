# from app.database import db_executions
# from keyboards import *
# from bot_aiogram import dp
# from steps import *
# import asyncio
# from aiogram import types, Dispatcher, Bot
# from keyboards import *
# from aiogram.types import ReplyKeyboardMarkup
# from aiogram.utils import executor, callback_data
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from keyboards import *
# @dp.message_handler(content_types=['text'], state=Steps.updating_state)
# async def up(message: types.Message):
#     if callback_data == '1':
#         await message.answer('Напишіть ваше ім’я і прізвище')
#         name_surname2 = message.text
#         await Steps.name_surname.set()
#         print('name_surname {}'.format(name_surname2))
