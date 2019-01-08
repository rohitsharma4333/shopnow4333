from flask import jsonify, g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app import db
from app.api import bp
from app.models.models import User
from app.api.errors import error_response


basicAuth = HTTPBasicAuth()
tokenAuth = HTTPTokenAuth()

#--------------------------------------------------------------------------------------

@basicAuth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()

    if(user is None):
        return(False)

    g.current_user = user

    return(user.check_password(password))

#--------------------------------------------------------------------------------------

@basicAuth.error_handler
def basic_auth_error():
    return(error_response(401))

#--------------------------------------------------------------------------------------

@bp.route('/tokens', methods=['POST'])
@basicAuth.login_required
def get_token():
    token = g.current_user.get_token()

    db.session.commit()

    return(jsonify({
        'token': token
    }))

#--------------------------------------------------------------------------------------

@tokenAuth.verify_token
def verify_token(token):
    g.current_user = User.check_token(token) if token else None
    return(g.current_user is not None)

#--------------------------------------------------------------------------------------

@tokenAuth.error_handler
def token_auth_error():
    return(error_response(401))