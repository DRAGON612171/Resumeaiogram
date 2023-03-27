from aiogram.dispatcher.filters.state import StatesGroup, State


class Steps(StatesGroup):
    name_surname = State()
    phone_number = State()
    email = State()
    education = State()