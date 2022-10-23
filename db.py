import mongoengine as me
import click

from flask import g
from . import models

def get_db():
    if 'db' not in g:
        g.db = me.connect('fmk_assignment', host='localhost', port=27017)
        print('Creating MongoDB connection')
    else:
        print('Found active MongoDB connection')
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
        print('Closed MongoDB Connection')

def init_db():
    None
    #TODO drop tables

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def create_user(user):
    db = get_db()
    user.save()
    print('User added to users collection')


def read_user(keyword):
    #Loop users
    for user in models.objects:
        #Loop the attributes of a user
        for atr in filter(lambda a: not a.startswith('__'), dir(user)):
            if atr == keyword:
                return user

def update_user():
    None

def delete_user(keyword):
    read_user(keyword).delete()

