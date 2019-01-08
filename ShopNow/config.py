import os

class AppConfig(object):
    # Secret key for WTF-Forms
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
                 'you-will-never-guess-it'

    # Database URL
    DB_ADMIN = os.environ.get('DATABASE_ADMIN') or \
               'shopnow_admin'
    DB_PASSWORD = os.environ.get('DATABASE_PASSWORD') or \
                 'shopnow_pwd1'
    DB_IP = os.environ.get('DATABASE_IP') or \
            'localhost'
    DB_NAME = os.environ.get('DATABASE_NAME') or \
              'shopnow_db'
    SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_ADMIN + ':' + DB_PASSWORD + '@' + DB_IP + '/' + DB_NAME

    # Set to track database modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Set to start Debugger
    DEBUGGER = True


class ErrorLogConfig(object):
    # Error log directory
    ERROR_LOG_DIR = 'logs/ShopNow.log'
    MAX_LOG_SIZE  = 10240
    BACKUP_COUNT  = 10
    ERROR_FORMAT  = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'

    # Create log directory if it doesn't exist
    if(not(os.path.exists(os.path.dirname(ERROR_LOG_DIR)))):
        os.mkdir(os.path.dirname(ERROR_LOG_DIR))
        open(x, ERROR_LOG_DIR).close()


class TokenConfig(object):
    TOKEN_EXPIRES_IN = os.environ.get('TOKEN_EXPIRES_IN') or \
                       3600
    TOKEN_BUFFER     = os.environ.get('TOKEN_BUFFER') or \
                       60