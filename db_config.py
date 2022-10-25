# for access to db

import os
import pathlib


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(pathlib.Path(__file__).parent.absolute(), 'COMPETITION.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTPLUS_VALIDATE = True
    LOGGER_LEVEL = 'DEBUG'
    SECRET_KEY = "secret-key-goes-here"
