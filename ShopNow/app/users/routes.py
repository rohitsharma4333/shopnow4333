from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.users.forms import SignUpForm, UpdatePasswordForm
from app.users import bp
from app.models.models import User

@bp.route('/signup', methods=['GET', 'POST'])
def signUp():
    if(current_user.is_anonymous):
        form = SignUpForm()

        if(form.validate_on_submit()):
            user = User(username=form.username.data, emailID=form.emailID.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            return(redirect(url_for('main.index')))
        else:
            return(render_template('signup.html', title='Sign Up', form=form))
    else:
        return (redirect(url_for('main.index')))

#----------------------------------------------------------------------------------------------9

@bp.route('/updatepassword', methods=['GET', 'POST'])
@login_required
def updatePassword():
    form = UpdatePasswordForm()

    if(form.validate_on_submit()):
        user = User.query.get(int(current_user.userID))
        user.set_password(form.password.data)
        db.session.commit()
        return(redirect(url_for('main.index')))
    return(render_template('updatepassword.html', title='Update User Details', form=form))