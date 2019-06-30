import psycopg2
import os
from flask import Flask, request, g
from urllib.parse import urlparse


def get_db():
    if 'db' not in g:
        url = urlparse(os.environ['DATABASE_URL'])
        username = url.username
        password = url.password
        database = url.path[1:]
        hostname = url.hostname
        
        g.db = psycopg2.connect(dbname=database,
                                user=username,
                                password=password,
                                host=hostname)
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
