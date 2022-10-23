import os

from flask import Flask
from flask_mongoengine import MongoEngine

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config['MONGODB_SETTINGS'] = {
        "db": "fmk_assignment",
        "host": "localhost",
        "port": 27017
    }
    #db = MongoEngine(app)
    #add command(optional)
    #from . import db
    #db.init_app(app)

    #add blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    # a simple page that says hello
    @app.route('/fmk/v1')
    def hello():
        #TODO return collection with api paths
        return 'Hello, World!'

    return app