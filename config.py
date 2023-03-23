import os
from dotenv import load_dotenv

load_dotenv()

Token = os.getenv('BOT_TOKEN')
ssh_username = os.getenv('SERVER_SHH_USERNAME')
ssh_password = os.getenv('SERVER_SSH_PASSWORD')
connect_password = os.getenv('SERVER_CONNECT_PASSWORD')
hostname = os.getenv('HOST_NAME')


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
