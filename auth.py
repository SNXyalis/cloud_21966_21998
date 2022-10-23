import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db, close_db

from .models import User

#TODO update url_prefix before upload
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = get_db()

        data=request.get_json()
        #username = data.get('username', '')
        #password = data.get('password', '')
        user = User(**data)
        #user =  User(username, password)
        user.save()

    return jsonify({'response': 'Added User'})


@bp.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    #delete_user(id)
    db = get_db()
    user = User.objects[0]
    user.delete()

    return jsonify({'response': 'Deleted User'})


@bp.route('/user/<id>')
def user(id):
    db = get_db()
    user = User.objects[0]
    #user = read_user(id)

    return jsonify({'username': user.username, 'password': user.password}), 200