from aiogram.dispatcher.filters.state import StatesGroup, State


class Steps(StatesGroup):
    name_surname = State()
    get_image = State()
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
    name_surname_edit = State()
    image_edit = State()
    phone_number_edit = State()
    email_edit = State()
    education_edit = State()
    tech_skills_edit = State()
    soft_skills_edit = State()
    projects_edit = State()
    lang_edit = State()
    lang_level_edit = State()
    country_edit = State()
    city_edit = State()
    edit_professions = State()
    profession_edit = State()
    description_edit = State()
    work_experience_edit = State()
    job_description_edit = State()
    how_long_edit = State()
    end_message_edit = State()
