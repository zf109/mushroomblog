import secrets
import os

from PIL import Image
from flask import Flask
from flask_login import LoginManager

from mushroom.persistence.db_manager import get_user
from .config import Config as conf

"""setting up basic facilitating functions"""
login_manager = LoginManager()
flask_app = Flask(conf.APP_NAME)

@login_manager.user_loader
def user_loader(user_id):
    """register user loading method to user_loader in login_manager"""
    return get_user(user_id)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    #TODO: change the hardcoded path to configuration
    picture_path = os.path.join(flask_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


"""bind the app to views/apis"""
from .server import add_apis, add_views

login_manager.init_app(flask_app)
flask_app.config.from_object(conf)
add_apis(flask_app)
add_views(flask_app)
