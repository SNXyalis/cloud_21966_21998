import mongoengine as me

def get_db():
    return me.connect('fmk_assignment', host='localhost', port=27017)


