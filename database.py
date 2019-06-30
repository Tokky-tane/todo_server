import psycopg2
import os
from flask import Flask, request, g


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(dbname=os.environ['DB_NAME'],
                                user=os.environ['DB_USER'],
                                password=os.environ['DB_PASSWORD'],
                                host=os.environ['DB_HOST'])
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
