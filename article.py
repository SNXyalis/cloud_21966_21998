from curses import keyname
import functools, requests
import json
from requests.exceptions import HTTPError
from urllib import response

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from .db import get_db

from .models import Article

#TODO update url_prefix before upload
bp = Blueprint('article', __name__, url_prefix='/article')

KEYWORDS_STR = [
    "Tesla", 
    "Microsoft", 
    "Apple",
    "Verizon",
    "Meta",
    "Coinbase",
    "Amazon",
    "Tencent"
]

@bp.route('/insert/<key>', methods=['GET', 'POST'])
def insert(key):
    if request.method == 'POST':
        db = get_db()
        try:
            response = requests.get('https://newsapi.org/v2/everything?q='+key+'&from=2022-10-21&sortBy=popularity&apiKey=dfa72c75b9ec4b3d8470b1786f586658')
            response.raise_for_status()
            data = json.loads(response.text)
            filtered_data = {
                'keyword': key,
                'articles': data['articles']
            }

            articles = Article(keyword=key, articles=data['articles'])

            if key.capitalize() in KEYWORDS_STR:
                articles.switch_collection(key.capitalize())
                articles.save()
                return jsonify({'response': 'Added Articles'})
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')

    return jsonify({'response': 'Failed to add articles'})

@bp.route('/get/<key>')
def articles(key):
    db = get_db()
    if key.capitalize() in KEYWORDS_STR:
        articles = Article.switch_collection(Article(), key.capitalize())
        from mongoengine.queryset import QuerySet
        new_objects = QuerySet(Article,articles._get_collection())
        d = {}
        for artcl in new_objects:
            d.update(json.loads(artcl.to_json()))
        return jsonify(d), 200
    return jsonify({'data': 'Error'})