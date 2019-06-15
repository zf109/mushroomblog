from mushroom.database.connection import db_session
from mushroom.persistence.db_manager import dataset_to_orms
from tests.data.generate import generate_dataset

def db_insert(users, posts, comments):
    with db_session() as sess:
        user_orms, post_orms, comment_orms = dataset_to_orms(sess=sess, users=users, posts=posts,comments=comments)
        [sess.add(u) for u in user_orms]
        [sess.add(p) for p in post_orms]
        [sess.add(c) for c in comment_orms]
        sess.commit()

        # have to run the second time, as foreign keys (author_id, post_id etc.) will not be set during first commit
        # for some reason sqlalchemy only allow set id when both original orm (say, user) and the connected orm (say, post)
        # are presented in database. There might be a better way to do this...
        user_orms, post_orms, comment_orms = dataset_to_orms(sess=sess, users=users, posts=posts,comments=comments)
        [sess.add(u) for u in user_orms]
        [sess.add(p) for p in post_orms]
        [sess.add(c) for c in comment_orms]
        sess.commit()

if __name__ == '__main__':

    users, posts, comments = generate_dataset(10, 10, 15, 5)
    db_insert(users, posts, comments)

