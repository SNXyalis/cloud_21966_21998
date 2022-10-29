from curses import keyname
import functools, requests
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

@bp.route('/insert/<keyword>', methods=['GET', 'POST'])
def insert(keyword):
    if request.method == 'POST':
        db = get_db()
        try:
            response = requests.get('https://newsapi.org/v2/everything?q='+keyword+'&from=2022-10-21&sortBy=popularity&apiKey=dfa72c75b9ec4b3d8470b1786f586658')
            response.raise_for_status()
            jsonResponse = response.json()
            articles = Article(**data)

            if keyword.capitalize() in KEYWORDS_STR:
                articles.switch_collection(keyword.capitalize())
                articles.save()
                return jsonify({'response': 'Added Articles'})
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')

    return jsonify({'response': 'Failed to add articles'})

@bp.route('/get/<keyword>')
def articles(keyword):
    db = get_db()
    if keyword.capitalize() in KEYWORDS_STR:
        articles = Article.switch_collection(Article(), keyword.capitalize())
        from mongoengine.queryset import QuerySet
        new_objects = QuerySet(Article,articles._get_collection())
        print(new_objects)

 #   return jsonify(articles.toDict()), 200