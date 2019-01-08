from flask import Flask
from config import AppConfig, ErrorLogConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler

# try:
#     x
#     print('its there')
# except:
#     print('not there')
# x=1

# Create db, migate and login variables
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.logIn'

# Create the APP
def create_app(appConfigClass=AppConfig, errorConfigClass=ErrorLogConfig):
    app = Flask(__name__)

    # Apply config to app
    app.config.from_object(appConfigClass)

    # Initialize all the global variables with app
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # Register all Blueprints
    # # errors blueprint
    # from app.errors import bp as errors_bp
    # app.register_blueprint(errors_bp, url_prefix='/errors')
    #
    # # auth blueprint
    # from app.auth import bp as auth_bp
    # app.register_blueprint(auth_bp, url_prefix='/auth')
    #
    # # users blueprint
    # from app.users import bp as users_bp
    # app.register_blueprint(users_bp, url_prefix='/users')
    #
    # # main blueprint
    # from app.main import bp as main_bp
    # app.register_blueprint(main_bp)

    # api blueprint
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Apply error log handler to app
    if(not(app.debug)):
        file_handler = RotatingFileHandler(ErrorLogConfig.ERROR_LOG_DIR,
                                           maxBytes=ErrorLogConfig.MAX_LOG_SIZE,
                                           backupCount=ErrorLogConfig.BACKUP_COUNT)
        file_handler.setFormatter(logging.Formatter(ErrorLogConfig.ERROR_FORMAT))
        file_handler.setLevel(logging.INFO)

        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('ShopNow Startup')
    return(app)

# Import models for Migration
from app.models import models