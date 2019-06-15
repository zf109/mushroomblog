from os import getenv


class Config(object):
    APP_NAME = "mushroom"
    CACHE_TYPE = getenv("CACHE_TYPE", "simple")
    USE_CACHE = int(getenv("USE_CACHE", True))
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'
