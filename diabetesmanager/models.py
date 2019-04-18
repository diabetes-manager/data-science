"""Connect to AWS RDS instance"""
from os import environ

import psycopg2


try:
    DB = psycopg2.connect(
        dbname=environ["DB_NAME"],
        user=environ["DB_USER"],
        password=environ["DB_PWD"],
        host=environ["DB_HOST"],
        connect_timeout=2
    )
except psycopg2.OperationalError as e:
    print(e)
    DB = None
