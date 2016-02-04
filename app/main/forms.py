from flask import flash, redirect, url_for
from flask.ext.login import login_user
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, ValidationError 
from wtforms.validators import Required, Email, Length, EqualTo, Regexp
from .. models import User

class LoginForm(Form):
    email = StringField('email@domain.com', validators=[Required(), Length(1, 64) ])
    password = PasswordField('password', validators=[Required()])

class SignupForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('username', validators=[Required(), Length(1,64), Regexp('^[a-zA-Z0-9][\._a-z0-9]*$', 0, 'Your username may start with an upper or lowercase letter. Only lowercase letters, numbers, underscores, and periods may follow.')])

    password = PasswordField('Password', validators = [Required(), EqualTo('password_confirmation', message='Your passwords must match.')]) 
    password_confirmation = PasswordField('Confirm Password', validators = [Required()])

    submit = SubmitField("Register")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already in use.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first() or User.query.filter_by(username=field.data.lower()).first():
            raise ValidationError('Username already taken')

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash("%s field: %s" % (getattr(form, field).label.text, error), 'danger')


def process_login(form):
    user = User.query.filter_by(email=form.email.data).first()
    if user is not None and user.check_password(form.password.data):
        login_user(user, True)
        flash('Welcome back, ' + user.username + '.', 'success')
        return redirect(url_for('main.index'))
    flash('Invalid email + password combination.', 'danger')
