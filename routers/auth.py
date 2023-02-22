from fastapi import APIRouter
from .models import User, Article, SDName,Article_request
from pydantic import BaseModel
from typing import List
from .db import get_db
from itertools import groupby
import json

router = APIRouter(
    prefix='/auth'
)

class Ruser(BaseModel):
    username: str
    password: str
    email: str
    city: str
    keywords: List[str]

    def toDict(self):
        return {
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "city": self.city,
            "keywords": self.keywords
        }

@router.post("/register")
def register(ruser: Ruser):
    db = get_db()
    user = User(**ruser.toDict())
    user.save()
    return {"response": "Added User"}

@router.delete("/delete/{email_param}")
def delete(email_param: str):
    db = get_db()
    for user in User.objects(email=email_param):
        try:
            user.delete()
        except Exception as er:
            print("{e}. Could not assign keywords to user during delete(email_param)")
    return {'response': 'Deleted User'}

@router.put("/update/{email_param}")
def update(email_param: str, ruser: Ruser):
    db = get_db()
    for user in User.objects(email=email_param):
        try:
            user.update(**ruser.toDict())
        except Exception as er:
            print("{e}. Could not assign keywords to user during update(email_param)")

    return {'response': 'Updated User'}

@router.get("/getMessage/{email_param}")  
def getMessage(email_param: str):

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

    return dict_to_json


@router.get("/getMessage/loc/{email_param}")  
def getMessage(email_param: str, ruser: Ruser):

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

    tmp_dict = { "city" : ruser.toDict().get("city") }
    article_request = Article_request(**tmp_dict)
    article_request.save()
        

    return dict_to_json