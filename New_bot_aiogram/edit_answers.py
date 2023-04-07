from aiogram import types
from bot_aiogram import dp, bot
from Resumeaiogram.database import db_executions


@dp.message_handler(content_types=['text'])
async def edit_name_surname(message: types.Message):
    try:
        await db_executions.add_name_surname(message.chat.id, message.text)
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(content_types=['text'])
async def edit_phone_number(message: types.Message):
    try:
        await db_executions.add_phone_number(message.chat.id, message.text)
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(content_types=['text'])
async def edit_email(message: types.Message):
    try:
        await db_executions.add_email(message.chat.id, message.text)
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(content_types=['text'])
async def edit_education(message: types.Message):
    try:
        await db_executions.add_education(message.chat.id, message.text)
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(content_types=['text'])
async def edit_soft_skills(message: types.Message):
    try:
        await db_executions.add_soft_skills(message.chat.id, message.text)
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(content_types=['text'])
async def edit_tech_skills(message: types.Message):
    try:
        await db_executions.add_tech_skills(message.chat.id, message.text)
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(content_types=['text'])
async def edit_projects(message: types.Message):
    try:
        await db_executions.add_projects(message.chat.id, message.text)
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(content_types=['text'])
async def edit_lang(message: types.Message):
    try:
        await db_executions.add_lang(message.chat.id, message.text)
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(content_types=['text'])
async def edit_lang_level(message: types.Message):
    try:
        await db_executions.add_lang_level(message.chat.id, message.text)
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(content_types=['text'])
async def edit_country(message: types.Message):
    try:
        await db_executions.add_country(message.chat.id, message.text)
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(content_types=['text'])
async def edit_city(message: types.Message):
    try:
        await db_executions.add_city(message.chat.id, message.text)
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(content_types=['text'])
async def edit_profession(message: types.Message):
    try:
        await db_executions.add_profession(message.chat.id, message.text)
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(content_types=['text'])
async def edit_description(message: types.Message):
    try:
        await db_executions.add_description(message.chat.id, message.text)
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(content_types=['text'])
async def edit_past_work(message: types.Message):
    try:
        await db_executions.add_past_work(message.chat.id, message.text)
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(content_types=['text'])
async def edit_job_description(message: types.Message):
    try:
        await db_executions.add_job_description(message.chat.id, message.text)
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')


@dp.message_handler(content_types=['text'])
async def edit_how_long(message: types.Message):
    try:
        await db_executions.add_how_long(message.chat.id, message.text)
        await bot.send_message(message.chat.id, 'Ваші дані оновлено')
    except:
        await bot.send_message(message.chat.id, 'Виникла помилка')
