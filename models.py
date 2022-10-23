import mongoengine as me

class User(me.Document):
    #DB configs
    meta = {'collection': 'users'}

    #Fields
    username=me.StringField(required=True)
    password=me.StringField(required=True)