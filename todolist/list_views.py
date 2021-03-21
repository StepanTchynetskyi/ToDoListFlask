import json

from flask import jsonify, Blueprint, request
from flask_http_response import success, error

urlu = Blueprint('list', __name__, url_prefix='/list')

from .models import ToDoList


@urlu.route('/<int:pk>/', methods=['GET', 'PUT', 'DELETE'])
def read_update_delete_by_id(pk):
    from custom_users.models import CustomUser
    if request.method == "GET":
        todo_list = ToDoList.get_by_id(pk=pk)
        if todo_list:
            return jsonify(todo_list.to_dict())
        return error.return_response(message="Error", status=400)
    if request.method == "PUT":
        todo_list = ToDoList.get_by_id(pk)
        if not todo_list:
            return error.return_response(message="Error", status=404)
        if not request.get_json():
            return error.return_response(message="Error", status=400)

        try:
            data = request.get_json()
        except json.JSONDecodeError:
            return error.return_response(message="Error", status=400)

        members_to_add = data.get('members_to_add')
        members_to_delete = data.get('members_to_delete')
        if members_to_add or members_to_delete:
            todo_list = todo_list.update_members(members_to_add, members_to_delete)
            if not todo_list:
                return error.return_response(message="Error", status=400)
        data = {'name': data.get('name'),
                'description': data.get('description')}

        todo_list = todo_list.update1(**data)
        if not todo_list:
            return error.return_response(message="Error", status=400)
        return success.return_response(message="Updated", status=201)
    if request.method == "DELETE":
        todo_list = ToDoList.get_by_id(pk)
        if not todo_list:
            return error.return_response(message="Error", status=404)

        ToDoList.remove(pk=pk)
        return success.return_response(message="Deleted", status=200)

@urlu.route('/', methods=['POST'])
def create():
    if request.method == "POST":
        from custom_users.models import CustomUser
        try:
            data = request.get_json()
        except json.JSONDecodeError:
            return error.return_response(message="Error", status=400)
        data = {
            'name': data.get('name'),
            'description': data.get('description') if data.get('description') else '',
            'members': [CustomUser.get_by_id(pk=user_id) for user_id in data.get('members')]
            if data.get('members') else None
        }

        todo_list = ToDoList.create(**data)
        if todo_list:
            return jsonify(todo_list.to_dict())
        return error.return_response(message="Error", status=400)