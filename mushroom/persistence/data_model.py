
from .utils import Saveable
from datetime import datetime
from uuid import uuid4

from mushroom.database.models import User as UserOrm, Post as PostOrm, Comment as CommentOrm


def _time2str(datetime_):
    return str(datetime_)


def _str2time(datetime_):
    return datetime.strptime(datetime_, '%Y-%m-%d %H:%M:%S.%f')


class User(Saveable):
    def __init__(self, id_=None, username=None, password=None, nickname=None,
                email=None, date_created=None, last_modified=None, image_file=None,
                posts=None, comments=None):
        self.id = id_ or str(uuid4())
        self.username = username
        self.password = password
        self.nickname = nickname
        self.email = email
        self.image_file = image_file or 'default.png'
        self.posts = posts or []
        self.comments = comments or []
        self.date_created = date_created or datetime.now()
        self.last_modified = last_modified or self.date_created

        self._post_ids = []
        self._comments_ids = []

    # the following 6 attributes are from flask UserMixn
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def __eq__(self, other):
        '''
        Checks the equality of two `UserMixin` objects using `get_id`.
        zf: modified this to use hasattr instead of UserMixin to allow duck typing
        '''
        if hasattr(other, 'get_id'):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        '''
        Checks the inequality of two `UserMixin` objects using `get_id`.
        '''
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal

    @property
    def post_ids(self):
        self._post_ids = [p.id for p in self.posts]
        return self._post_ids

    @post_ids.setter
    def post_ids(self, val):
        self._post_ids = val
        return self._post_ids

    @property
    def comment_ids(self):
        self._comments_ids = [c.id for c in self.comments]
        return self._comments_ids

    @comment_ids.setter
    def comment_ids(self, val):
        self._comments_ids = val
        return self._comments_ids

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'nickname': self.nickname,
            'email': self.email,
            'date_created': _time2str(self.date_created),
            'last_modified': _time2str(self.last_modified),
            'post_ids': self.post_ids,
            'comment_ids': self.comment_ids,
            'image_file': self.image_file,
        }

    @classmethod
    def from_dict(cls, dict_):
        instance = cls(
            id_=dict_['id'],
            username=dict_['username'],
            password=dict_['password'],
            nickname=dict_['nickname'],
            email=dict_['email'],
            image_file=dict_['image_file'],
            date_created=_str2time(dict_['date_created']),
            last_modified=_str2time(dict_['last_modified']),
        )

        instance.post_ids = dict_['post_ids']
        instance.comment_ids = dict_['comment_ids']
        return instance

    def to_orm(self, user_orm=None):
            if user_orm:
                user_orm.username = self.username
                user_orm.nickname = self.nickname
                user_orm.password = self.password
                user_orm.email = self.email
                user_orm.image_file = self.image_file
                user_orm.last_modified = self.last_modified
            else:
                user_orm = UserOrm(
                    id=self.id,
                    username=self.username,
                    nickname=self.nickname,
                    password=self.password,
                    email=self.email,
                    image_file=self.image_file,
                    date_created=self.date_created,
                    last_modified=self.last_modified
                )
            return user_orm

    @classmethod
    def from_orm(cls, user_orm: UserOrm, posts=None, comments=None):
        return cls(
            id_=user_orm.id,
            username=user_orm.username,
            nickname=user_orm.nickname,
            password=user_orm.password,
            email=user_orm.email,
            image_file=user_orm.image_file,
            date_created=user_orm.date_created,
            last_modified=user_orm.last_modified,
            posts=posts or [],
            comments=comments or []
        )

    def __repr__(self):
        return f'<User {self.username}>'


class Post(Saveable):
    def __init__(self, author=None, id_=None, title=None, body=None, date_created=None,
                last_modified=None, like_count=None, comments=None,):
        self.id = id_ or str(uuid4())
        self.title = title
        self.body = body
        self.date_created = date_created or datetime.now()
        self.last_modified = last_modified or self.date_created
        self.like_count = like_count or 0

        self.comments = comments or []
        self.author = author

        self._author_id = None
        self._comment_ids = []

    @property
    def author_id(self):
        if self.author:
            self._author_id = self.author.id
        return self._author_id

    @author_id.setter
    def author_id(self, val):
        self._author_id = val
        return self._author_id

    @property
    def comment_ids(self):
        return [c.id for c in self.comments]

    @comment_ids.setter
    def comment_ids(self, val):
        if self.comments:
            self._comment_ids = [c.id for c in self.comments]
        return self._comment_ids

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'date_created': _time2str(self.date_created),
            'last_modified': _time2str(self.last_modified),
            'like_count': self.like_count,
            'author_id': self.author_id,
            'comment_ids': self.comment_ids,
        }

    @classmethod
    def from_dict(cls, dict_):
        instance = cls(
            id_=dict_['id'],
            title=dict_['title'],
            body=dict_['body'],
            date_created=_time2str(dict_['date_created']),
            last_modified=_time2str(dict_['last_modified']),
            like_count=dict_['like_count'],
        )

        instance.author_id = dict_['author_id']
        instance.comment_ids = dict_['comment_ids']
        return instance

    def to_orm(self, post_orm=None, author_orm=None):
        # if orm exists, then you don't update date created and author
        if post_orm:
            post_orm.title = self.title
            post_orm.body = self.body
            post_orm.last_modified = self.last_modified
        else:
            # assert author_orm, f'post must have an author, author_orm cannot be {type(author_orm)} type'
            post_orm = PostOrm(
                id=self.id,
                author= author_orm,
                title=self.title,
                body=self.body,
                like_count=self.like_count,
                date_created=self.date_created,
                last_modified=self.last_modified,
            )
        return post_orm

    @classmethod
    def from_orm(cls, post_orm: PostOrm, author=None, comments=None):
        """
        create post object from database orm, it does not fetch the linked orm though,
        these are passed as argument, like author and comments
        """
        return cls(
            id_=post_orm.id,
            title=post_orm.title,
            body=post_orm.body,
            like_count=post_orm.like_count,
            date_created=post_orm.date_created,
            last_modified=post_orm.last_modified,
            author=author,
            comments=comments or [],
        )

    def __repr__(self):
        return '<Post %r>'%(self.title)


class Comment(Saveable):

    def __init__(self, id_=None, post=None, author=None, body=None, date_created=None,
                last_modified=None, like_count=None):
        self.id = id_ or str(uuid4())
        self.body = body
        self.date_created = date_created or datetime.now()
        self.last_modified = last_modified or self.date_created
        self.like_count = like_count or 0

        self.post = post
        # self.post_id = post_id or post.id
        self.author = author
        # self.author_id = author_id or self.author.id

    @property
    def post_id(self):
        return self.post.id

    @property
    def author_id(self):
        return self.author.id

    def to_dict(self):
        return {
            'id': self.id,
            'body': self.body,
            'date_created': _time2str(self.date_created),
            'last_modified': _time2str(self.last_modified),
            'like_count': self.like_count,
            'post_id': self.post_id,
            'author_id': self.author_id,
        }

    @classmethod
    def from_dict(cls, dict_):
        cls(
            id_=dict_['id'],
            body=dict_['body'],
            date_created=_str2time(dict_['date_created']),
            last_modified=_str2time(dict_['last_modified']),
            like_count=dict_['like_count'],
            # post_id=dict_['post_id'],
            # author_id=dict_['author_id'],
        )

    def to_orm(self, comment_orm=None, author_orm=None, post_orm=None):
        if comment_orm:
            comment_orm.body = self.body
            comment_orm.last_modified = self.last_modified
        else:
            # assert author_orm, f'comment must have an author, author_orm cannot be {type(author_orm)} type'
            # assert post_orm, f'comment must have an author, post_orm cannot be {type(post_orm)} type'
            comment_orm = CommentOrm(
                id=self.id,
                body=self.body,
                post=post_orm,
                author=author_orm,
                like_count=self.like_count,
                date_created=self.date_created,
                last_modified=self.last_modified,
            )
        return comment_orm

    @classmethod
    def from_orm(cls, comment_orm: CommentOrm, author=None, post=None):
        return cls(
            id_=comment_orm.id,
            body=comment_orm.body,
            like_count=comment_orm.like_count,
            date_created=comment_orm.date_created,
            last_modified=comment_orm.last_modified,
            author=author,
            post=post,
        )


    def __repr__(self):
        return f'<Comments: {self.body[:40]}...>'

