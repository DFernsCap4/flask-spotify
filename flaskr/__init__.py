import os
from flask import Flask
from flask_migrate import Migrate
from flaskr.db import db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'flaskr.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize the database with the app
    db.init_app(app)

    # Set up Flask-Migrate
    migrate = Migrate(app, db)

    from flaskr import models  # Import your models here to ensure they are registered
    from flaskr import auth
    from flaskr import song

    app.register_blueprint(auth.bp)
    app.register_blueprint(song.bp)

    return app
