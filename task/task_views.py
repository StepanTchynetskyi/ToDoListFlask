import json
from flask import jsonify, Blueprint, request
from flask_http_response import success, error

urlu = Blueprint('task', __name__, url_prefix='/task')

from .models import Tasks


@urlu.route('/<int:pk>/', methods=['GET', 'PUT', 'DELETE'])
def read_update_delete_by_id(pk):
    if request.method == "GET":
        task = Tasks.get_by_list_id(pk)
        # not working properly
        tasks ={}
        for i in range(len(list(task))):
            tasks[i] = task[i].to_dict()
        return jsonify(tasks)
    if request.method == "PUT":
        # not working
        if not request.get_json():
            return error.return_response(message="Error", status=400)

        try:
            body = request.get_json()
        except json.JSONDecodeError:
            return error.return_response(message="Error", status=400)

        task_data = {
            'title': body.get('title'),
            'description': body.get('description'),
            'deadline': body.get('deadline'),
            'user_id': body.get('user_id'),
            'list_id': body.get('list_id'),
            'is_completed': body.get('list_id'),
        }
        task = Tasks.get_by_id(pk=pk)
        print(task)
        if not task:
            return error.return_response(message="Error", status=400)
        try:
            task.update(**task_data)
            return jsonify(task.to_dict())
        # Invalid input
        except (ValueError, TypeError):
            return error.return_response(message="Error", status=400)
    if request.method =="DELETE":
        task = Tasks.get_by_id(pk)
        if task:
            Tasks.remove(pk)
            return success.return_response(message="User successfully deleted", status=200)
        return error.return_response(message='User not found', status=400)

@urlu.route('/', methods=['POST'])
def create():
    if request.method == "POST":
        if not request.get_json():
            error.return_response(message="Error", status=400)

        try:
            body = request.get_json()
        except json.JSONDecodeError:
            return error.return_response(message="Error", status=400)

        task_data = {
            'title': body.get('title'),
            'description': body.get('description'),
            'deadline': body.get('deadline'),
            'user_id': body.get('user_id'),
            'list_id': body.get('list_id'),
        }
        task = Tasks.create(**task_data)
        if task:
            return success.return_response("Created", status=201)
        return error.return_response("Error",status=400)
