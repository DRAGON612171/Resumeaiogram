from aiogram.dispatcher.filters.state import StatesGroup, State


class Steps(StatesGroup):
    name_surname = State()
    phone_number = State()
    email = State()
    education = State()
    tech_skills = State()
    soft_skills = State()
    projects = State()
    lang = State()
    lang_level = State()
    country = State()
    city = State()
    profession = State()
    description = State()
    past_work = State()
    how_long = State()
    job_description = State()


