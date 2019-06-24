import datetime
import dateutil.parser
from flask import Flask, request, Response
from flask_api import status
from database import close_db
from crud_task import get_all_tasks, delete_all_tasks, create_task, delete_user_tasks, get_user_tasks, delete_task, get_task, update_task
from crud_user import get_all_users, delete_all_users, create_user, get_user, update_user, delete_user

app = Flask(__name__)
app.teardown_appcontext(close_db)


@app.route('/users', methods=['GET', 'POST', 'DELETE'])
def route_users():
    if request.method == 'GET':
        users = get_all_users()
        return users

    elif request.method == 'POST':
        name = request.json['name']
        password = request.json['password']
        id = create_user(name, password)

        location = '/users/{}'.format(id)
        response = create_post_response(location)
        return response

    else:
        delete_all_users()
        return '', status.HTTP_204_NO_CONTENT


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def route_user(user_id):
    if request.method == 'GET':
        user = get_user(user_id)
        return user

    elif request.method == 'PUT':
        name = request.json['name']
        password = request.json['password']

        update_user(user_id, name, password)

        return '', status.HTTP_200_OK

    else:
        delete_user(user_id)
        return '', status.HTTP_200_OK


@app.route('/tasks', methods=['GET', 'DELETE'])
def route_tasks():
    if request.method == 'GET':
        tasks = get_all_tasks()
        return tasks

    else:
        delete_all_tasks()
        return '', status.HTTP_204_NO_CONTENT


@app.route('/users/<int:user_id>/tasks', methods=['GET', 'POST', 'DELETE'])
def route_users_tasks(user_id):
    if request.method == 'GET':
        tasks = get_user_tasks(user_id)
        return tasks
    elif request.method == 'POST':
        title = request.json['title']
        due_date = request.json['due_date']

        if(due_date is not None):
            due_date = dateutil.parser.parse(due_date)

        id = create_task(user_id, title, due_date)
        location = '/users/{}/tasks/{}'.format(user_id, id)
        response = create_post_response(location)

        return response
    else:
        delete_user_tasks(user_id)
        return '', status.HTTP_200_OK


@app.route('/users/<int:user_id>/tasks/<int:task_id>', methods=['GET', 'PUT', 'DELETE'])
def route_task(user_id, task_id):
    if request.method == 'GET':
        task = get_task(task_id)
        return task
    elif request.method == 'PUT':
        title = request.json['title']
        due_date = request.json['due_date']

        update_task(task_id, title, due_date)

        return '', status.HTTP_200_OK
    else:
        delete_task(task_id)
        return '', status.HTTP_200_OK


def create_post_response(location):
    res = Response('')
    res.headers['location'] = location
    return res
