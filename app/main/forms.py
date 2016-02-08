##
# Forms file
# Contains forms and validators
##
from flask import flash, redirect, url_for
from flask.ext.login import login_user
from flask.ext.wtf import Form, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, ValidationError, IntegerField, DecimalField
from wtforms.validators import Required, Email, Length, EqualTo, Regexp, NumberRange
from .. models import User
from . import main
from datetime import datetime


## 
# LoginForm to be displayed on the navbar
##
class LoginForm(Form):
    email = StringField('email@domain.com', validators=[Required(), Length(1, 64) ])
    password = PasswordField('password', validators=[Required()])


##
# SignupForm for '/register'
##
class SignupForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('username', validators=[Required(), Length(1,64), Regexp('^[a-zA-Z0-9][\._a-z0-9]*$', 0, 
        'Your username may start with an upper- or lowercase letter or a number. Only lowercase letters, numbers, underscores, and periods may follow.')])

    password = PasswordField('Password', validators = [Required(), EqualTo('password_confirmation', message='Your passwords must match.')]) 
    password_confirmation = PasswordField('Confirm Password', validators = [Required()])

    submit = SubmitField("Register")
    
    # Uncomment to enable ReCaptcha for registration
    ## captcha = RecaptchaField()

    # Check if email already exists
    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already in use.')

    # Check if username exists
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first() or User.query.filter_by(username=field.data.lower()).first():
            raise ValidationError('Username already taken.')

##
# BookForm form for '/add' + editing books
##
class BookForm(Form):
    title = StringField('Title', validators=[Required(), Length(1,128)])
    author = StringField('Author', validators=[Required(), Length(1,128)])
    condition = IntegerField('Condition', validators=[Required(), NumberRange(1,5)])
    isbn = IntegerField('ISBN13', validators=[Required(), NumberRange(0,9999999999999)])
    price = DecimalField('Price', validators=[Required(), NumberRange(0, 8888.8)])

    submit = SubmitField("Save")

##
# Collect errors from form fields
# flash to user
##
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash("%s field: %s" % (getattr(form, field).label.text, error), 'danger')


##
# Check LoginForm data against db
# Log in user if checks pass
##
def process_login(form):
    user = User.query.filter_by(email=form.email.data.lower()).first()
    if user is not None and user.check_password(form.password.data):
        login_user(user, True)
        user.last_online = datetime.utcnow()
        flash('Welcome back, ' + user.username + '.', 'success')
        return True

    flash('Invalid email + password combination.', 'danger')
    return False
