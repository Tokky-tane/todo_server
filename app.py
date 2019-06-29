import os
import datetime
import dateutil.parser
from flask import Flask, request, Response
from flask_api import status
from database import close_db
from crud_task import get_all_tasks, delete_all_tasks, create_task, delete_user_tasks, get_user_tasks, delete_task, get_task, update_task
from crud_user import get_all_users, delete_all_users, create_user, get_user, update_user, delete_user
import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)
app.teardown_appcontext(close_db)

cred = credentials.Certificate({
    "type": os.environ['FIREBASE_TYPE'],
    "project_id": os.environ['FIREBASE_PROJECT_ID'],
    "private_key_id": os.environ['FIREBASE_PRIVATE_KEY_ID'],
    "private_key": os.environ['FIREBASE_PRIVATE_KEY'].replace(r'\\n',r'\n'),
    "client_email": os.environ['FIREBASE_CLIENT_EMAIL'],
    "client_id": os.environ['FIREBASE_CLIENT_ID'],
    "auth_uri": os.environ['FIREBASE_AUTH_URI'],
    "token_uri": os.environ['FIREBASE_TOKEN_URI'],
    "auth_provider_x509_cert_url": os.environ['FIREBASE_AUTH_PROVIDER_CERT_URL'],
    "client_x509_cert_url": os.environ['FIREBASE_CLIENT_CERT_URL']
})
firebase_admin.initialize_app(cred)


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


@app.route('/users/<string:user_id>/tasks', methods=['GET', 'POST', 'DELETE'])
def route_users_tasks(user_id):
    token = request.headers.get('Authorization')
    try:
        decoded_token = auth.verify_id_token(token)
        if not decoded_token['uid'] == user_id:
            return '', status.HTTP_401_UNAUTHORIZED
    except ValueError:
        return '', status.HTTP_401_UNAUTHORIZED
    except auth.AuthError:
        return '', status.HTTP_401_UNAUTHORIZED

    if request.method == 'GET':
        tasks = get_user_tasks(decoded_token['uid'])
        return tasks
    elif request.method == 'POST':
        title = request.json['title']
        due_date = request.json['due_date']

        if(due_date is not None):
            due_date = dateutil.parser.parse(due_date)

        id = create_task(user_id, title, due_date)
        location = '/users/{}/tasks/{}'.format(decoded_token['uid'], id)
        response = create_post_response(location)

        return response
    else:
        delete_user_tasks(decoded_token['uid'])
        return '', status.HTTP_200_OK


@app.route('/users/<string:user_id>/tasks/<int:task_id>', methods=['GET', 'PUT', 'DELETE'])
def route_task(user_id, task_id):
    token = request.headers.get('Authorization')
    try:
        auth.verify_id_token(token)
        decoded_token = auth.verify_id_token(token)
        if not decoded_token['uid'] == user_id:
            return '', status.HTTP_401_UNAUTHORIZED

    except ValueError:
        return '', status.HTTP_401_UNAUTHORIZED
    except auth.AuthError:
        return '', status.HTTP_401_UNAUTHORIZED

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
        return '', status.HTTP_204_NO_CONTENT


def create_post_response(location):
    res = Response('')
    res.headers['location'] = location
    return res
