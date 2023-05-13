from io import BytesIO
import requests
from flask import render_template, redirect, url_for, session as ses, make_response, request
from Resumeaiogram.app.forms import LoginForm, Download
from Resumeaiogram.app import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from Resumeaiogram.database.SQLAlchemy_connection import ResumeBot


db = create_engine('postgresql://poop402r:3IC8RGJaHmQs@ep-bitter-paper-853686.eu-central-1.aws.neon.tech/neondb')
Base = declarative_base()
Session = sessionmaker(db)
session = Session()


@app.route('/generate_pdf', methods=['GET', 'POST'])
def generate_pdf():
    if request.method == 'POST':
        form = Download()
        right_tuple = ses['right_tuple']

        # Получите данные для формирования PDF
        name_surname = right_tuple["name_surname"]
        phone_number = right_tuple["phone_number"]
        email = right_tuple["email"]
        education = right_tuple["education"]
        lang = right_tuple["lang"]
        lang_level = right_tuple["lang_level"]
        country = right_tuple["country"]
        city = right_tuple["city"]
        description = right_tuple["description"]
        profession = right_tuple["profession"]
        soft_skills = right_tuple["soft_skills"]
        tech_skills = right_tuple["tech_skills"]
        projects = right_tuple["projects"]
        how_long = right_tuple["how_long"]
        job_description = right_tuple["job_description"]
        past_work = right_tuple["past_work"]

        html_content = render_template('download_file.html', profession=profession, name_surname=name_surname,
                                       phone_number=phone_number, email=email, education=education,
                                       tech_skills=tech_skills, soft_skills=soft_skills, projects=projects,
                                       lang=lang, lang_level=lang_level, country=country, city=city,
                                       past_work=past_work, how_long=how_long, job_description=job_description,
                                       description=description, form=form)

        # Конвертирование HTML в PDF с помощью PDFShift
        pdfshift_api_key = '626843b335cd41388ff64c0c4bb36deb'
        response = requests.post('https://api.pdfshift.io/v3/convert/pdf',
                                 json={'source': html_content},
                                 auth=('api', pdfshift_api_key),
                                 )

        # Проверка успешности конвертации
        if response.status_code == 200:
            # Получение PDF в байтовом формате
            pdf_bytes = response.content

            # Отправка PDF пользователю
            pdf_file = BytesIO(pdf_bytes)
            response = make_response(pdf_file.getvalue())
            response.headers["Content-Type"] = "application/pdf"
            response.headers["Content-Disposition"] = "attachment; filename=Resume.pdf"
            return response
        else:
            # Обработка ошибки конвертации
            return "Error occurred during PDF generation."

    else:
        # Обработка GET-запроса
        return render_template('index.html')


@app.route("/", methods=['GET', 'POST'])
@app.route("/index/", methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        result = []
        users = session.query(ResumeBot).all()
        for i in users:
            result.append(
                {
                "id": i.id,
                "name_surname" : i.name_surname,
                "phone_number" : i.phone_number,
                "email": i.email,
                "education" : i.education,
                "lang" : i.lang,
                "lang_level" : i.lang_level,
                "country" : i.country,
                "city" : i.city,
                "description" : i.description,
                "profession" : i.profession,
                "soft_skills": i.soft_skills,
                "tech_skills": i.tech_skills,
                "projects": i.projects,
                "how_long" : i.how_long,
                "job_description" : i.job_description,
                "past_work" : i.past_work,
                "password" : i.password,
                }
            )
        for data_tuple in result:
            if int(form.user_id.data) == int(data_tuple["id"]):
                if str(data_tuple["password"]) == str(form.password.data):
                    ses['right_tuple'] = data_tuple
                    return redirect(url_for('resume'))
                else:
                    error = 'Невірний логін або пароль'

    return render_template('login_form.html', form=form, error=error)


@app.route("/resume", methods=['GET', 'POST'])
def resume():
    print(0)
    form = Download()
    if 'right_tuple' not in ses:
        return redirect(url_for('login'))

    right_tuple = ses['right_tuple']
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
    if form.validate_on_submit():
        right_tuple = ses['right_tuple']
        return redirect(url_for('generate_pdf'))

    def portal():
        nonlocal name_surname, phone_number, email, education, tech_skills, soft_skills, projects, lang, lang_level, \
                            country, city, past_work, description, profession, how_long, job_description
        name_surname = right_tuple["name_surname"]
        phone_number = right_tuple["phone_number"]
        email = right_tuple["email"]
        education = right_tuple["education"]
        lang = right_tuple["lang"]
        lang_level = right_tuple["lang_level"]
        country = right_tuple["country"]
        city = right_tuple["city"]
        description = right_tuple["description"]
        profession = right_tuple["profession"]
        soft_skills = right_tuple["soft_skills"]
        tech_skills = right_tuple["tech_skills"]
        projects = right_tuple["projects"]
        how_long = right_tuple["how_long"]
        job_description = right_tuple["job_description"]
        past_work = right_tuple["past_work"]

    portal()

    return render_template('index.html', profession=profession, name_surname=name_surname, phone_number=phone_number,
                           email=email, education=education, tech_skills=tech_skills, soft_skills=soft_skills,
                           projects=projects, lang=lang, lang_level=lang_level, country=country, city=city,
                           past_work=past_work, how_long=how_long, job_description=job_description,
                           description=description, form=form)


