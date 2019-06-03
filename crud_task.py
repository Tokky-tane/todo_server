import datetime
from database import get_db
from psycopg2.extras import RealDictCursor
import json


def get_all_tasks():
    with get_db() as db:
        with db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                        SELECT id, user_id, title, deadline FROM tasks
                        """)
            tasks = format_tasks(cur.fetchall())

            return json.dumps(tasks, indent=2)


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
                        SELECT id, user_id, title, deadline FROM tasks
                        WHERE user_id = %s
                        """, (user_id,))

            tasks = format_tasks(cur.fetchall())

            return json.dumps(tasks, indent=2)


def delete_user_tasks(user_id):
    with get_db() as db:
        with db.cursor() as cur:
            cur.execute("""
                        DELETE FROM tasks
                        WHERE user_id = %s
                        """, (user_id,))
            return


def create_task(user_id, title, deadline):
    with get_db() as db:
        with db.cursor() as cur:
            cur.execute("""
                        INSERT INTO tasks (user_id, title, deadline)
                        VALUES (%s, %s,%s)
                        RETURNING id
                        """, (user_id, title, deadline))
            id = cur.fetchone()[0]
            return id


def get_task(id):
    with get_db() as db:
        with db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                        SELECT id, user_id, title, deadline FROM tasks
                        WHERE id = %s
                        """, (id,))

            task = convert_timestamp(cur.fetchone())

            return json.dumps(task, indent=2)


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


def format_tasks(tasks):
    for task in tasks:
        convert_timestamp(task)
    return tasks


def convert_timestamp(task):
    if task['deadline'] is not None:
        task['deadline'] = task['deadline'].isoformat()

    return task
