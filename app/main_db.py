import psycopg2
import sshtunnel
import json
from Resumeaiogram.config import *


def rewrite(right):
    a = right.replace('[', '{')
    b = a.replace(']', '}')
    return b


def writeTable(id, name_surname, phone_number, email, education, lang, lang_level, country, city, password, description,
    profession, soft_skills, tech_skills, projects, how_long, job_description, past_work):
    sshtunnel.SSH_TIMEOUT = 10.0
    sshtunnel.TUNNEL_TIMEOUT = 10.0
    postgres_hostname = hostname
    postgres_host_port = 13055
    try:
        with sshtunnel.SSHTunnelForwarder(('ssh.pythonanywhere.com'),
                ssh_username=ssh_username,
                ssh_password=ssh_password,
                remote_bind_address=(postgres_hostname, postgres_host_port)) as tunnel:
            connection = psycopg2.connect(
                user='super', password=connect_password,
                host='127.0.0.1', port=tunnel.local_bind_port,
                database='postgres')
            cur = connection.cursor()
            cur.execute("""INSERT INTO public.resume_db(
                            id, name_surname, phone_number, email, education, lang, lang_level, country, city, password,
                            description, profession, soft_skills, tech_skills, projects, how_long, job_description, past_work)
                            VALUES ({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');""".format(id,
                            name_surname, phone_number, email, rewrite(json.dumps(education, ensure_ascii=False)), rewrite(json.dumps(lang, ensure_ascii=False)), rewrite(json.dumps(lang_level, ensure_ascii=False)),
                            country, city, password,
                            description, profession, rewrite(json.dumps(soft_skills, ensure_ascii=False)), rewrite(json.dumps(tech_skills, ensure_ascii=False)), rewrite(json.dumps(projects, ensure_ascii=False)),
                            rewrite(json.dumps(how_long, ensure_ascii=False)), rewrite(json.dumps(job_description, ensure_ascii=False)), rewrite(json.dumps(past_work, ensure_ascii=False))))

            connection.commit()
            connection.close()
            cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def readTable():
    sshtunnel.SSH_TIMEOUT = 10.0
    sshtunnel.TUNNEL_TIMEOUT = 10.0
    postgres_hostname = hostname
    postgres_host_port = 13055
    try:
        with sshtunnel.SSHTunnelForwarder(('ssh.pythonanywhere.com'),
                ssh_username=ssh_username,
                ssh_password=ssh_password,
                remote_bind_address=(postgres_hostname, postgres_host_port)) as tunnel:
            connection = psycopg2.connect(
                user='super', password=connect_password,
                host='127.0.0.1', port=tunnel.local_bind_port,
                database='postgres')
            cur = connection.cursor()
            cur.execute("""SELECT *
            FROM public.resume_db;""")
            result = cur.fetchall()
            print(result)
            connection.close()
            cur.close()
            return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


