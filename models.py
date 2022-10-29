import email, time
from random import choices
from email.policy import default
import mongoengine as me

#News API dfa72c75b9ec4b3d8470b1786f586658
#API: "https://newsapi.org/v2/everything?q="+KEYWORD+"&from=2022-10-21&sortBy=popularity&apiKey="+ API_KEY

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