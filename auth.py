import functools, json
from itertools import groupby

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db, close_db

from .models import User, Article, SDName

#TODO update url_prefix before upload
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = get_db()

        data=request.get_json()
        user = User(**data)
        user.save()

    return jsonify({'response': 'Added User'})


@bp.route('/getMessage/<email_param>', methods=['GET'])
def getMessage(email_param):

    db = get_db()
    k_words = None

    for user in User.objects(email=email_param):
        try:
            k_words = user.keywords
        except Exception as er:
            print("{e}. Could not assign keywords to user during getMessage(email_param)")

    print(k_words)


    L = []
    key_func = lambda x: x[0]

    for entry in k_words:#For every user keyword
        from mongoengine.queryset import QuerySet
        articles = Article.switch_collection(Article(), entry.capitalize())#Switch to the collection
        new_objects = QuerySet(Article,articles._get_collection())#Query all the document of the keyword
        d = {} #Documents in Python Object form
        for artcl in new_objects:
            d.update(json.loads(artcl.to_json()))#Format BSON to Python Object


        article_obj = d['articles'] #Array of articles
        for elem in article_obj: #For every document get source name and article
            L.append((elem['source']['name'], elem))
        

    L = sorted(L, key=key_func)
    dict_to_json = []
    for key, group in groupby(L, key_func):#Group articles per SDN
            
        articles = []
        for i in list(group): #Filtering a tuple to get only the article without the key
            articles.append(i[1])


        sdn_description = None
        for el in SDName.objects(name=key):
            sdn_description = el.description
            break
        
        #print(key + " :", articles, "Description: ",sdn_description, sep="\n")
        
        dict_to_json.append({
            "SourceName": key,
            "Description": sdn_description,
            "articles": articles
        })

    return jsonify(dict_to_json)


@bp.route('/delete/<email_param>', methods=['DELETE'])
def delete(email_param):
    #delete_user(id)
    db = get_db()
    for user in User.objects(email=email_param):
        try:
            user.delete()
        except Exception as er:
            print("{e}. Could not assign keywords to user during getMessage(email_param)")

    return jsonify({'response': 'Deleted User'})


@bp.route('/user/<email_param>')
def user(email_param):
    db = get_db()
    u = None
    for user in User.objects(email=email_param):
        try:
            u = user.toDict()
        except Exception as er:
            print("{e}. Could not assign keywords to user during getMessage(email_param)")


    return jsonify(u), 200