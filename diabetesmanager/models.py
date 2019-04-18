"""Connect to AWS RDS instance"""
from os import environ

from dotenv import load_dotenv
load_dotenv()
from .config import Config

import psycopg2

print('environ:', environ)

if environ['FLASK_ENV'] == 'production':
    DB = psycopg2.connect(
        dbname=environ["DB_NAME"],
        user=environ["DB_USER"],
        password=environ["DB_PWD"],
        host=environ["DB_HOST"],
    )
else:
    DB = None
