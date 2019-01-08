from flask import jsonify, g, request
from sqlalchemy import or_
from app import db
from app.api import bp
from app.models.models import User
from app.api.auth import tokenAuth
from app.api.errors import bad_request, error_response

@bp.route('/users/<int:id>', methods=['GET'])
@tokenAuth.login_required
def get_user(id):
    return(jsonify(User.query.get_or_404(int(id)).to_dict()))

#--------------------------------------------------------------------------------------

@bp.route('/users', methods=['GET'])
@tokenAuth.login_required
def get_users():
    # users = User.query.all().to_dict()
    data = User.to_collection_dict(User.query.all, 'api.get_users')
    return(jsonify(data))

#--------------------------------------------------------------------------------------

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}

    if('username' not in data or 'emailID' not in data or 'password' not in data):
        return(bad_request('username, emailID, password should be present.'))

    user = User.query.filter(or_(User.username==data['username'], User.emailID==data['emailID'])).first()
    if(user is not None):
        return(bad_request('username and emailID should be unique, please select new.'))

    user = User()
    user.from_dict(data, newUser=True)

    db.session.add(user)
    db.session.commit()

    return(jsonify(user.to_dict()))

#--------------------------------------------------------------------------------------

@bp.route('/users/<int:id>', methods=['PUT'])
@tokenAuth.login_required
def update_user(id):
    if(g.current_user.userID != id):
        return(error_response(403))

    data = request.get_json() or {}
    g.current_user.from_dict(data)

    db.session.add(g.current_user)
    db.session.commit()

    return(jsonify(g.current_user.to_dict()))

#--------------------------------------------------------------------------------------