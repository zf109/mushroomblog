from os import getenv

class Config():
    DATABASE_URL = getenv("DATABASE_URL")
    SCHEMA = 'mushroom'
    LOG_LEVEL = getenv("LOG_LEVEL", "INFO")
