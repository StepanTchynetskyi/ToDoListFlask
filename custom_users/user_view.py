import json

from flask import jsonify, Blueprint, request
from flask_http_response import success, error

urlu = Blueprint('user', __name__, url_prefix='/user')

from .models import CustomUser


@urlu.route('/<int:pk>/', methods=['GET', 'PUT', 'DELETE'])
def read_update_delete_by_id(pk):
    if request.method == "GET":
        user = CustomUser.get_by_id(pk=pk)
        if user:
            return jsonify(user.to_dict())
        return error.return_response(message="Error", status=400)

    if request.method == 'PUT':
        user = CustomUser.get_by_id(pk=pk)

        if not user:
            return error.return_response(message="Error", status=404)

        if not request.get_json():
            return error.return_response(message="Error", status=400)

        try:
            body = request.get_json()
        except json.JSONDecodeError:
            return error.return_response(message="Error", status=400)
        updated_user = CustomUser.update(user, **body)

        if updated_user:
            return jsonify(user.to_dict())
        return error.return_response(message="Error", status=400)

    if request.method == 'DELETE':
        user = CustomUser.get_by_id(pk)
        if user:
            CustomUser.remove(pk)
            return success.return_response(message="User successfully deleted", status=200)
        return error.return_response(message='User not found', status=400)


@urlu.route("/", methods=['POST'])
def create():
    if request.method == "POST":
        if not request.get_json():
            error.return_response(message="Error", status=400)

        try:
            body = request.get_json()
        except json.JSONDecodeError:
            return error.return_response(message="Error", status=400)

        data = {'first_name': body.get('first_name'),
                'last_name': body.get('last_name'),
                'password': body.get('password'),
                'email': body.get('email')}

        new_user = CustomUser.create(**data)
        if new_user:
            return jsonify(new_user.to_dict())
        return error.return_response(message="Error", status=400)
