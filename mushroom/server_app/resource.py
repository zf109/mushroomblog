
import os
from flask_restful import Resource, request
from flask_httpauth import HTTPBasicAuth
from .config import Config as server_conf
from ..config import Config as pkg_conf
from ..log import setuplogger

_logger = setuplogger(__name__)


class BlogPost(Resource):
    def post(self):
        """
        Create a blog post
        """
        pass

    def get(self):
        """
        Query for a blog post
        """
        pass
    
    def put(self):
        """
        update a blog post
        """
        pass
