import email, time
from email.policy import default
import mongoengine as me

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