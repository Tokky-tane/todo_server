from database import get_db
from psycopg2.extras import RealDictCursor
import json


def get_all_users():
    with get_db() as db:
        with db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
            SELECT * FROM users
            """)
            return json.dumps(cur.fetchall(), indent=2)


def delete_all_users():
    with get_db() as db:
        with db.cursor() as cur:
            cur.execute("""
                        DELETE FROM users
                        """)
            return


def create_user(name, password):
    with get_db() as db:
        with db.cursor() as cur:
            cur.execute("""
                        INSERT INTO users (name, password)
                        VALUES (%s, %s)
                        RETURNING id
                        """, (name, password))
            id = cur.fetchone()[0]
            return id


def get_user(id):
    with get_db() as db:
        with db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                        SELECT * FROM users
                        WHERE id = %s
                        """, (id,))
            return json.dumps(cur.fetchone(), indent=2)


def update_user(id, name, password):
    with get_db() as db:
        with db.cursor() as cur:
            cur.execute("""
                        UPDATE users 
                        SET name=%s, password=%s
                        WHERE id=%s
                        """, (name, password, id))
            return


def delete_user(id):
    with get_db() as db:
        with db.cursor() as cur:
            cur.execute("""
                        DELETE FROM users 
                        WHERE id = %s
                        """, (id,))
            return
