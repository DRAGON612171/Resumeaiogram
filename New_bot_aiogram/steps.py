from aiogram.dispatcher.filters.state import StatesGroup, State


class Steps(StatesGroup):
    name_surname = State()
    # updating_state = State()
    phone_number = State()
    get_email = State()
    get_education = State()
    get_tech_skills = State()
    get_soft_skills = State()
    get_projects = State()
    get_lang = State()
    get_lang_level = State()
    get_country = State()
    get_city = State()
    get_profession = State()
    get_description = State()
    get_work_experience = State()
    get_job_description = State()
    get_how_long = State()
    end_message = State()




