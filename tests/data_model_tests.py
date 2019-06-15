from unittest import TestCase, main
from logging import getLogger, CRITICAL, WARNING, INFO, DEBUG, basicConfig
from os import getenv
from uuid import uuid4
from datetime import datetime

from mushroom.persistence.data_model import User

basicConfig()
_logger = getLogger("unittest")
loglevels = {
    "CRITICAL": CRITICAL,
    "WARNING": WARNING,
    "INFO": INFO,
    "DEBUG": DEBUG,
    '': INFO
}
_logger.setLevel(loglevels[getenv("LOG_LEVEL", "INFO")])


class UserDataModelTestCase1(TestCase):
    def test_from_dict(self):
        user1 = User(
            id_='565ab4c5-ccac-4489-894a-dc22cc6c468a',
            username='user1',
            nickname='mushroom the cat',
            password='this should not be the password',
            email='truffle@mushroom.cat',
            date_created=datetime.strptime('2019-06-03 00:35:36.212573', '%Y-%m-%d %H:%M:%S.%f')
        )

        expected_dict = {
            'id': '565ab4c5-ccac-4489-894a-dc22cc6c468a',
            'username': 'user1',
            'password': 'this should not be the password',
            'nickname': 'mushroom the cat',
            'email': 'truffle@mushroom.cat',
            'date_created': '2019-06-03 00:35:36.212573',
            'last_modified': '2019-06-03 00:35:36.212573',
            'post_ids': [],
            'comment_ids': []
        }
        assert user1.to_dict() == expected_dict


class PostDataModelTestCase1(TestCase):
    def test_from_dict(self):
        user1 = User(
            id_='565ab4c5-ccac-4489-894a-dc22cc6c468a',
            username='user1',
            nickname='mushroom the cat',
            password='this should not be the password',
            email='truffle@mushroom.cat',
            date_created=datetime.strptime('2019-06-03 00:35:36.212573', '%Y-%m-%d %H:%M:%S.%f')
        )

        expected_dict = {
            'id': '565ab4c5-ccac-4489-894a-dc22cc6c468a',
            'username': 'user1',
            'password': 'this should not be the password',
            'nickname': 'mushroom the cat',
            'email': 'truffle@mushroom.cat',
            'date_created': '2019-06-03 00:35:36.212573',
            'last_modified': '2019-06-03 00:35:36.212573',
            'post_ids': [],
            'comment_ids': []
        }
        assert user1.to_dict() == expected_dict


class CommentDataModelTestCase1(TestCase):
    def test_from_dict(self):
        user1 = User(
            id_='565ab4c5-ccac-4489-894a-dc22cc6c468a',
            username='user1',
            nickname='mushroom the cat',
            password='this should not be the password',
            email='truffle@mushroom.cat',
            date_created=datetime.strptime('2019-06-03 00:35:36.212573', '%Y-%m-%d %H:%M:%S.%f')
        )

        expected_dict = {
            'id': '565ab4c5-ccac-4489-894a-dc22cc6c468a',
            'username': 'user1',
            'password': 'this should not be the password',
            'nickname': 'mushroom the cat',
            'email': 'truffle@mushroom.cat',
            'date_created': '2019-06-03 00:35:36.212573',
            'last_modified': '2019-06-03 00:35:36.212573',
            'post_ids': [],
            'comment_ids': []
        }
        assert user1.to_dict() == expected_dict

