from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required
from werkzeug.urls import url_parse
# from app import db
from app.auth.forms import LoginForm
from app.auth import bp
from app.models.models import User

@bp.route('/login', methods=['GET', 'POST'])
def logIn():
    form = LoginForm()
    if(form.validate_on_submit()):
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return(redirect(url_for('auth.logIn')))
        else:
            login_user(user, remember=form.rememberMe.data)
            nextPage = request.args.get('next')
            if(not nextPage or url_parse(nextPage).netloc != ''):
                nextPage = url_for('main.index')
            return(redirect(nextPage))
    else:
        return render_template('login.html', title='Log In', form=form)

#----------------------------------------------------------------------------------------------

@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logOut():
    logout_user()
    return(redirect(url_for('main.index')))