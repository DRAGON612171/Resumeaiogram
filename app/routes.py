import asyncio
from Resumeaiogram.app import app
from flask import render_template, redirect, url_for, session, flash
from flask_login import current_user
from .forms import LoginForm
from Resumeaiogram.database.db_executions import select_all
from .models import User


@app.route("/", methods=['GET', 'POST'])
@app.route("/index/", methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        result = asyncio.run(select_all())
        user = User.query.filter_by(user_id=form.user_id.data).first()
        if user.password != form.password.data:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        for data_tuple in result:
            if int(form.user_id.data) in data_tuple and str(data_tuple[-1]) == str(form.password.data):
                session['right_tuple'] = data_tuple
                return redirect(url_for('resume'))
    return render_template('login_form.html', form=form)


@app.route("/resume", methods=['GET', 'POST'])
def resume():
    if 'right_tuple' not in session:
        return redirect(url_for('login'))

    right_tuple = session['right_tuple']
    profession = ''
    name_surname = ''
    phone_number = ''
    email = ''
    education = ''
    tech_skills = ''
    soft_skills = ''
    projects = ''
    lang = ''
    lang_level = ''
    country = ''
    city = ''
    past_work = ''
    how_long = ''
    job_description = ''
    description = ''

    def portal():
        nonlocal name_surname, phone_number, email, education, tech_skills, soft_skills, projects, lang, lang_level, \
                            country, city, past_work, description, profession, how_long, job_description
        name_surname = right_tuple[1]
        phone_number = right_tuple[2]
        email = right_tuple[3]
        education = right_tuple[4].split(',')
        lang = right_tuple[5]
        lang_level = right_tuple[6]
        country = right_tuple[7]
        city = right_tuple[8]
        description = right_tuple[9]
        profession = right_tuple[10]
        soft_skills = right_tuple[11].split(',')
        tech_skills = right_tuple[12].split(',')
        projects = right_tuple[13].split(',')
        how_long = right_tuple[14]
        job_description = right_tuple[15]
        past_work = right_tuple[16]

    portal()

    return render_template('index.html', profession=profession, name_surname=name_surname, phone_number=phone_number,
                           email=email, education=education, tech_skills=tech_skills, soft_skills=soft_skills,
                           projects=projects, lang=lang, lang_level=lang_level, country=country, city=city,
                           past_work=past_work, how_long=how_long, job_description=job_description, description=description)