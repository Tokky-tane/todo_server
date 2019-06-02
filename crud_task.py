from database import get_db
from psycopg2.extras import RealDictCursor
import json


def get_all_tasks():
    with get_db() as db:
        with db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                        SELECT id, user_id, title FROM tasks
                        """)
            return json.dumps(cur.fetchall(), indent=2)


def delete_all_tasks():
    with get_db() as db:
        with db.cursor() as cur:
            cur.execute("""
                        DELETE FROM tasks
                        """)
            return


def get_user_tasks(user_id):
    with get_db() as db:
        with db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                        SELECT id, user_id, title FROM tasks 
                        WHERE user_id = %s
                        """, (user_id,))
            return json.dumps(cur.fetchall(), indent=2)


def delete_user_tasks(user_id):
    with get_db() as db:
        with db.cursor() as cur:
            cur.execute("""
                        DELETE FROM tasks 
                        WHERE user_id = %s
                        """, (user_id,))
            return


def create_task(user_id, title):
    with get_db() as db:
        with db.cursor() as cur:
            cur.execute("""
                        INSERT INTO tasks (user_id, title)
                        VALUES (%s, %s)
                        RETURNING id
                        """, (user_id,title))
            id = cur.fetchone()[0]
            return id


def get_task(id):
    with get_db() as db:
        with db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                        SELECT id, user_id, title FROM tasks 
                        WHERE id = %s
                        """, (id,))
            return json.dumps(cur.fetchone(), indent=2)


def update_task(id, title):
    with get_db() as db:
        with db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                        UPDATE tasks
                        SET title = %s
                        WHERE id = %s
                        """, (title, id))
            return


def delete_task(id):
    with get_db() as db:
        with db.cursor() as cur:
            cur.execute("""
                        DELETE FROM tasks
                        WHERE id = %s
                        """, (id,))
            return
