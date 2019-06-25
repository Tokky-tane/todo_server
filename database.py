import psycopg2
import os
from flask import Flask, request, g


def get_db():
    db_password = os.environ['DB_PASSWORD']
    if 'db' not in g:
        g.db = psycopg2.connect(dbname='sample',
                                user='postgres',
                                password=db_password)
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
