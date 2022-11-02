import pathlib
import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://ibis_competition:IBIS_COMPETITION12@localhost:3306/ibis_competition?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTPLUS_VALIDATE = True
    LOGGER_LEVEL = 'DEBUG'
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    # EXECUTOR_MAX_WORKERS = 1
    # UPLOAD_FOLDER = os.path.join(pathlib.Path(__file__).parent.absolute(), 'files')
