from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, message, chat, message_id
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from steps import *
from config import *


bot = Bot(token=Token)
dp = Dispatcher(bot, storage=MemoryStorage())


def but_create():
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = KeyboardButton('📄Створити резюме📄')
    reply_markup.add(but1)
    return reply_markup


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id, '👋Привіт!👋\n'  
                                            '😃Це бот для створення резюме, думаю тобі сподобається😃'.format(message.from_user.first_name), reply_markup=but_create())

@dp.message_handler(state=None, content_types=['text'])
async def message_reply (message: types.Message):
    if message.text == '📄Створити резюме📄':
        reply_markup1 = ReplyKeyboardMarkup(resize_keyboard=True)
        await bot.send_message(message.chat.id, 'Напишіть ваше ім’я і прізвище', reply_markup=reply_markup1)
        item = message.text
        await Steps.name_surname.set()
        await Steps.next()
        print('Name {}'.format(item))



@dp.message_handler(state=Steps.phone_number)
async def message_reply (message: types.Message):
    await bot.send_message(message.chat.id, 'Напишіть ваш номер телефону')
    item1 = message.text
    await Steps.phone_number.set()
    await Steps.next()
    print('number {}'.format(item1))




@dp.message_handler(state=Steps.email)
async def message_reply (message: types.Message):
    await bot.send_message(message.chat.id, 'Напишіть ваш email')
    item2 = message.text
    await Steps.email.set()
    await Steps.next()
    print('email {}'.format(item2))

@dp.message_handler(state=Steps.education )
async def message_reply(message: types.Message):
    await bot.send_message(message.chat.id, 'Напишіть рівень вашої освіти')
    item3 = message.text
    await Steps.education.set()
    await Steps.next()
    print('education {}'.format(item3))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)