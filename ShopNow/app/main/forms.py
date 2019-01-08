from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models.models import User

class LoginForm(FlaskForm):
    username   = StringField('Username', validators=[DataRequired()])
    password   = PasswordField('Password', validators=[DataRequired()])
    rememberMe = BooleanField('Remember Me')
    submit     = SubmitField('Sign In')

#--------------------------------------------------------------------------------------------

class SignUpForm(FlaskForm):
    username   = StringField('Username', validators=[DataRequired()])
    emailID    = StringField('Email ID', validators=[DataRequired(), Email()])
    password   = PasswordField('Password', validators=[DataRequired()])
    password2  = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit     = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if(user is not None):
            raise ValidationError('Please select different username')

    def validate_emailID(self, emailID):
        user = User.query.filter_by(emailID=emailID.data).first()
        if(user is not None):
            raise ValidationError('Please select different email address')