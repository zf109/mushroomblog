from datetime import datetime

from .models import User, Post
from .connection import db_session

def get_latest_posts(n=10):
    with db_session() as sess:
        sess.query(Post)
