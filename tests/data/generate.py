import json
import os

from essential_generators import DocumentGenerator
from uuid import uuid4
from random import randint, sample
from mushroom.persistence.data_model import User, Post, Comment
from itertools import product


def rand_passwd():
    valid_chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+'
    return ''.join(sample(valid_chars, randint(6,20)))


def get_email(username):
    email_providers = {'google', 'yahoo', 'hotmail', 'mushroom'}
    return '.'.join(username.lower().split()) + '@' + sample(email_providers, 1)[0] + '.com'


def get_dummy_posts(n=10, gen=None, author: User=None):
    gen = gen or DocumentGenerator()
    return [Post(
        author=author,
        title=gen.sentence(),
        body=gen.paragraph(),
        like_count=randint(0, 100)
    ) for _ in range(n)]


def get_dummy_comments(n=10, gen=None, author: User=None):
    gen = gen or DocumentGenerator()
    return [Comment(
        author=author,
        body=gen.paragraph(),
        like_count=randint(0, 100)
    ) for _ in range(n)]


def generate_dataset(n_user, n_posts, n_comments, var):

    gen = DocumentGenerator()
    users = []
    for _ in range(n_user):
        nickname = gen.name()
        user = User(
            username=nickname.lower().replace(' ', '_'),
            nickname=nickname,
            password=rand_passwd(),
            email=get_email(nickname)
        )

        posts = get_dummy_posts(n=n_posts+randint(-var, var), gen=gen, author=user)
        comments = get_dummy_comments(n=n_comments+randint(-var, var), gen=gen, author=user)
        user.posts, user.comments = posts, comments

        users.append(user)

    posts = [p for user in users for p in user.posts]
    comments = [c for user in users for c in user.comments]

    # attach comments to posts
    for comment in comments:
        post = sample(posts, 1)[0]
        post.comments.append(comment)
        comment.post = post
    return users, posts, comments


if __name__ == '__main__':
    """
        n_user: number of dummy users
        n_posts: average number of dummy posts per user
        n_comments: average number of dummy comments per user
        var: variation around number of posts/comments per user
    """

    n_user, n_posts, n_comments, var = 10, 10, 20, 5
    print(f'generate dataset with n_user: {n_user}')

    users, posts, comments = generate_dataset(n_user, n_posts, n_comments, var)

    # save to json file under a uniquely named folder
    version_dir = os.path.join('./tests/data/', 'dummy_ '+ str(uuid4()))
    os.mkdir(version_dir)
    file_map = {'user': users, 'post': posts, 'comment': comments}
    for name in file_map:
        path = os.path.join(version_dir, f'{name}.json')
        with open(path, 'w') as f:
            json.dump([item.to_dict() for item in file_map[name]], f)
