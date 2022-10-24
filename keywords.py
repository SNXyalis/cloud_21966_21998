from ast import keyword
import functools

from flask import (
    Blueprint, request, jsonify
)
from .db import get_db

from .models import Keyword

#TODO update url_prefix before upload
bp = Blueprint('keywords', __name__, url_prefix='/keywords')


@bp.route('/set', methods=['GET', 'POST'])
def set():
    if request.method == 'POST':
        db = get_db()

        data=request.get_json()
        keywords = Keyword(**data)
        keywords.save()

    return jsonify({'response': 'Initialized Keywords'})


@bp.route('/get', methods=['GET'])
def get(id):
    db = get_db()
    keywords = Keyword.objects[0]

    return jsonify(keywords.toDict())

