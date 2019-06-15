from mushroom.database.models import Post as PostOrm, User as UserOrm, Comment as CommentOrm
from mushroom.database.connection import db_session

from .data_model import User, Post, Comment
from ..log import setuplogger

_logger = setuplogger(__name__)

def dataset_to_orms(sess, users: [User]=None, posts: [Post]=None, comments: [Comment]=None):

    user_orms, post_orms, comment_orms = [], [], []

    for user in users:
        user_orm = sess.query(UserOrm).get(user.id)
        user_orm = user.to_orm(user_orm=user_orm)
        user_orms.append(user_orm)

    for post in posts:
        post_orm = sess.query(PostOrm).get(post.id)
        post_orm = post.to_orm(post_orm=post_orm)
        post_orm.author_id = post.author_id
        post_orms.append(post_orm)

    for comment in comments:
        comment_orm = sess.query(CommentOrm).get(comment.id)
        comment_orm = comment.to_orm(comment_orm=comment_orm)
        comment_orm.post_id = comment.post_id
        comment_orm.author_id = comment.author_id
        comment_orms.append(comment_orm)

    return user_orms, post_orms, comment_orms


"""
    level 1 deep into relationship to load
"""


def load_user_lv1(user_orm: UserOrm):
    if not user_orm:
        return None
    return User.from_orm(
        user_orm=user_orm,
        posts=[Post.from_orm(p) for p in user_orm.posts],
        comments=[Comment.from_orm(c) for c in user_orm.comments]
    )


def load_post_lv1(post_orm: PostOrm):
    return Post.from_orm(
        post_orm,
        author=User.from_orm(post_orm.author),
        comments=[Comment.from_orm(comment_orm, author=User.from_orm(comment_orm.author)) 
                    for comment_orm in post_orm.comments]
    )


"""
    highest level queries from database
"""

def load_latest_posts(n=10):
    with db_session() as sess:
        post_orms = sess.query(PostOrm).order_by('last_modified desc').limit(n)
        return [load_post_lv1(post_orm) for post_orm in post_orms]


"""
   posts interaction
"""

def get_post(post_id):
    with db_session() as sess:
        _logger.info(f'fetching post with id: {post_id}')
        post_orm = sess.query(PostOrm).get(post_id)
        return load_post_lv1(post_orm)


def save_post(post:Post):
    with db_session() as sess:
        post_orm = sess.query(PostOrm).get(post.id)
        post_orm = post.to_orm(post_orm=post_orm)
        sess.add(post_orm)
        sess.commit()


def filter_post(field, value, first=False):
    pass


def create_post(title, body, author):
    with db_session() as sess:
        author_orm = sess.query(UserOrm).get(author.id)
        post_orm = Post(title=title, body=body, author=author).to_orm(author_orm=author_orm)
        sess.add(post_orm)
        sess.commit()


def delete_post(post_id):
    with db_session() as sess:
        post_orm = sess.query(PostOrm).get(post_id)
        sess.delete(post_orm)
        sess.commit()


"""
   user interaction
"""

def get_user(user_id):
    with db_session() as sess:
        _logger.info(f'fetching user with id: {user_id}')
        user_orm = sess.query(UserOrm).get(user_id)
        return load_user_lv1(user_orm)


def save_user(user: User):
    with db_session() as sess:
        user_orm = sess.query(UserOrm).get(user.id)
        user_orm = user.to_orm(user_orm)
        sess.add(user_orm)
        sess.commit()


def filter_user(field, value, first=False):
    with db_session() as sess:
        user_orms = sess.query(UserOrm).filter(getattr(UserOrm, field) == value)
        users = [User.from_orm(u) for u in user_orms]
        if first:
            return users[0] if users else None
        return users


def create_user(username, nickname, password, email):
    with db_session() as sess:
        user_orm = User(username=username, nickname=nickname,
                password=password, email=email).to_orm()
        sess.add(user_orm)
        sess.commit()


def delete_user(user_id):
    pass
