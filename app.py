import os
import datetime
import dateutil.parser
from flask import Flask, request, Response
from flask_api import status
from database import close_db
from crud_task import get_all_tasks, delete_all_tasks, create_task, delete_user_tasks, get_user_tasks, delete_task, get_task, update_task, exist_task
import firebase_admin
from firebase_admin import credentials, auth
from dotenv import find_dotenv, load_dotenv

app = Flask(__name__)
app.teardown_appcontext(close_db)
load_dotenv(find_dotenv())

cred = credentials.Certificate({
    "type": os.environ['FIREBASE_TYPE'],
    "project_id": os.environ['FIREBASE_PROJECT_ID'],
    "private_key_id": os.environ['FIREBASE_PRIVATE_KEY_ID'],
    "private_key": os.environ['FIREBASE_PRIVATE_KEY'].replace('\\n', '\n'),
    "client_email": os.environ['FIREBASE_CLIENT_EMAIL'],
    "client_id": os.environ['FIREBASE_CLIENT_ID'],
    "auth_uri": os.environ['FIREBASE_AUTH_URI'],
    "token_uri": os.environ['FIREBASE_TOKEN_URI'],
    "auth_provider_x509_cert_url": os.environ['FIREBASE_AUTH_PROVIDER_CERT_URL'],
    "client_x509_cert_url": os.environ['FIREBASE_CLIENT_CERT_URL']
})
firebase_admin.initialize_app(cred)


@app.route('/users/me/tasks', methods=['GET', 'POST', 'DELETE'])
def route_users_tasks():
    token = request.headers.get('Authorization')
    try:
        user_id = auth.verify_id_token(token)['uid']
    except ValueError:
        return '', status.HTTP_401_UNAUTHORIZED
    except auth.AuthError:
        return '', status.HTTP_401_UNAUTHORIZED

    if request.method == 'GET':
        updated_at_min = request.args.get('updated_at_min')

        datetime_updated_at_min = None
        if(updated_at_min is not None):
            datetime_updated_at_min = dateutil.parser.isoparse(updated_at_min)

        tasks = get_user_tasks(user_id, datetime_updated_at_min)

        response = Response(mimetype='applicaiotn/json')
        response.set_data(tasks)
        return response

    elif request.method == 'POST':
        title = request.json['title']
        due_date = request.json['due_date']

        if(due_date is not None):
            due_date = dateutil.parser.isoparse(due_date)

        id = create_task(user_id, title, due_date)
        location = '/users/me/tasks/{}'.format(id)
        response = Response(status=status.HTTP_201_CREATED)
        response.headers['location'] = location

        return response

    else:
        delete_user_tasks(user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


@app.route('/users/me/tasks/<int:task_id>', methods=['GET', 'PUT', 'DELETE'])
def route_task(task_id):
    token = request.headers.get('Authorization')
    try:
        auth.verify_id_token(token)
    except ValueError:
        return '', status.HTTP_401_UNAUTHORIZED
    except auth.AuthError:
        return '', status.HTTP_401_UNAUTHORIZED

    if exist_task(task_id) == False:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        task = get_task(task_id)

        response = Response(mimetype='application/json')
        response.set_data(task)
        return response

    elif request.method == 'PUT':
        title = request.json['title']
        due_date = request.json['due_date']

        update_task(task_id, title, due_date)

        return '', status.HTTP_200_OK

    else:
        delete_task(task_id)
        return '', status.HTTP_204_NO_CONTENT
