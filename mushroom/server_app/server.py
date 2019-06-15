from flask import Flask
from flask_restful import Api as RestfulApi
import os
from logging import getLogger

from mushroom.server_app.resource import BlogPost
from .config import Config as conf

import  mushroom.server_app.views as v

_logger = getLogger("server")

def add_apis(app):
    pass
    # rest_api = RestfulApi(app, catch_all_404s=True)
    # rest_api.add_resource(BlogPost, '/api/v0.1/<string:model_name>/<string:version>/predict')

def add_views(app):
    app.add_url_rule('/', view_func=v.IndexView.as_view('index'), endpoint='alt_index')
    app.add_url_rule('/post/create', view_func=v.PostCreateView.as_view('create_post'))
    app.add_url_rule('/post/<string:post_id>', view_func=v.PostDetailView.as_view('post'))
    app.add_url_rule('/post/<string:post_id>/update', view_func=v.PostUpdateView.as_view('update_post'))
    app.add_url_rule('/post/<string:post_id>/delete', view_func=v.PostDeleteView.as_view('delete_post'))
    app.add_url_rule('/index', view_func=v.IndexView.as_view('index'))
    app.add_url_rule('/login', view_func=v.LoginView.as_view('login'))
    app.add_url_rule('/logout', view_func=v.LogoutView.as_view('logout'))
    app.add_url_rule('/home', view_func=v.HomeView.as_view('home'))
    app.add_url_rule('/account', view_func=v.AccountView.as_view('account'))
    app.add_url_rule('/about', view_func=v.AboutView.as_view('about'))
    app.add_url_rule('/register', view_func=v.RegisterView.as_view('register'))
