from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import url_for
from app import db, login
import base64, os
from config import TokenConfig


class APIMixin(object):
    @staticmethod
    def to_collection_dict(query, endPoint, **kwargs):
        resources = query()
        data = {
            'items': [item.to_dict() for item in resources],
            'total_items': len(resources),
            '_links':{
                'self': url_for(endPoint, **kwargs)
            }
        }
        return(data)

#--------------------------------------------------------------------------------------

# Users table
class User(APIMixin, UserMixin, db.Model):
    __tablename__ = 'users'

    userID           = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username         = db.Column(db.String(64), unique=True, index=True)
    emailID          = db.Column(db.String(100), unique=True, index=True)
    passwordHash     = db.Column(db.String(128))
    lastSeen         = db.Column(db.DateTime, default=datetime.utcnow())
    authorized       = db.Column(db.Boolean, default=False)
    agreements       = db.relationship('AgreementHeader', backref='customer', lazy='dynamic')
    token            = db.Column(db.String(32), index=True)
    token_expiration = db.Column(db.DateTime, default=datetime.utcnow() - timedelta(seconds=1))


    def __repr__(self):
        return('<User {}>'.format(self.username))


    def set_password(self, password):
        self.passwordHash = generate_password_hash(password)


    def check_password(self, password):
        return(check_password_hash(self.passwordHash, password))


    def get_id(self):
        return(self.userID)

    @staticmethod
    def get_unique_token():
        isUniqueToken = False

        while (not (isUniqueToken)):
            uniqueToken = base64.b64encode(os.urandom(24)).decode('utf-8')
            if (User.query.filter_by(token=uniqueToken).first() is None):
                isUniqueToken = True

        return (uniqueToken)


    def get_token(self):
        now = datetime.utcnow()

        if(self.token and self.token_expiration > now + timedelta(seconds=TokenConfig.TOKEN_BUFFER)):
            return(self.token)

        self.token = User.get_unique_token()
        self.token_expiration = now + timedelta(seconds=TokenConfig.TOKEN_EXPIRES_IN)

        return(self.token)


    def revokeToken(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)


    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()

        if(user is None or user.token_expiration < datetime.utcnow()):
            return(None)

        return(user)


    def to_dict(self, includeEmail=False):
        data = {
            "userID": self.userID,
            "username": self.username,
            "lastSeen": self.lastSeen,
            "authorized": self.authorized,
            "_links": {
                "self": url_for('api.get_user', id=self.userID)
            }
        }
        if (includeEmail):
            data["emailID"] = self.emailID

        return(data)


    def from_dict(self, data, newUser=False, changePassword=False, verifyUser=False):
        fields = ['username', 'emailID']
        for field in fields:
            if(field in data):
                setattr(self, field, data[field])

        if((changePassword or newUser) and 'password' in data):
            self.set_password(data['password'])

        if(verifyUser and 'authorized' in data):
            setattr(self, 'authorized', data['authorized'])

        return(self)

#--------------------------------------------------------------------------------------

@login.user_loader
def load_user(id):
    return (User.query.get(int(id)))

#--------------------------------------------------------------------------------------

class AgreementHeader(db.Model):
    __tablename__ = 'fnagrhd'

    comp_id   = db.Column(db.String(10), primary_key=True)
    agr_code  = db.Column(db.String(10), primary_key=True)
    agr_seq   = db.Column(db.Integer, primary_key=True)
    userID    = db.Column(db.Integer, db.ForeignKey('users.userID'))

    def __repr__(self):
        return('<Company {} Agreement {} Sequence{}>'.format(self.comp_id, self.agr_code, self.agr_seq))

#--------------------------------------------------------------------------------------