import email, time
from random import choices
from email.policy import default
import mongoengine as me
from fastapi import APIRouter

#News API dfa72c75b9ec4b3d8470b1786f586658
#API: "https://newsapi.org/v2/everything?q="+KEYWORD+"&from=2022-10-21&sortBy=popularity&apiKey="+ API_KEY


router = APIRouter(
    prefix='/auth'
)

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

class Article_request(me.Document):
    city=me.StringField(max_length=100, required=True)
    timestamp=me.StringField(default=str(time.time()))

    def toDict(self):
        return {
            'city': self.city,
            'timestamp': self.timestamp
        }


class User(me.Document):
    #DB configs
    meta = {'collection': 'users'}

    #Fields
    username=me.StringField(max_length=100, required=True) #Optional
    password=me.StringField(max_length=100, required=True) #Optional
    email=me.EmailField(max_length=100, unique=True, required=True)
    city=me.StringField(max_length=100, required=True)
    timestamp=me.StringField(default=str(time.time()))
    keywords=me.ListField(me.StringField(max_length=50))    


    def toDict(self):
        return {
            'username': self.username,
            'password': self.password, 
            'email': self.email, 
            'city': self.city, 
            'timestamp': self.timestamp, 
            'keywords': self.keywords
            }


class Keyword(me.Document):

    meta = {'collection': 'keywords'}

    keywords=me.ListField(me.StringField(max_length=50), 
        default=[
            "Tesla", 
            "Microsoft", 
            "Apple",
            "Verizon",
            "Meta",
            "Coinbase",
            "Amazon",
            "Tencent"
            ])
    
    def toDict(self):
        return {
            'keywords': self.keywords
        }

class Article(me.Document):

    keyword=me.StringField(max_length=50, choices=KEYWORDS_STR)
    articles=me.ListField(me.DictField())
    
    def toDict(self):
        return {
            'articles': self.articles
        }

class SingleArticle(me.Document):
    author=me.StringField(max_length=200000)
    content=me.StringField(max_length=200000)
    description=me.StringField(max_length=200000)
    publishedAt=me.StringField(max_length=200000)
    source=me.DictField()
    title=me.StringField(max_length=200000)
    url=me.StringField(max_length=200000)
    urlToImage=me.StringField(max_length=200000)

    def toDict(self):
        return {
            'author': self.author,
            'content': self.content,
            'description': self.description,
            'publishedAt': self.publishedAt,
            'source': self.source,
            'title': self.title,
            'url': self.url,
            'urlToImage': self.urlToImage
        }


class SDName(me.Document):
    name=me.StringField(max_length=50)
    description=me.StringField(max_length=200000)

    def toDict(self):
        return {
            'name': self.name,
            'description': self.description
        }