from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, ValidationError 
from wtforms.validators import Required, Email, Length, EqualTo, Regexp
from .. models import User

class LoginForm(Form):
    email = StringField('email@domain.com', validators=[Required(), Length(1, 64) ])
    password = PasswordField('password', validators=[Required()])

class SignupForm(Form):
    email = StringField('email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('username', validators=[Required(), Length(1,64), Regexp('^[a-zA-Z0-9][\._a-z0-9]*$', 0, 'Your username may start with an upper or lowercase letter. Only lowercase letters, numbers, underscores, and periods may follow')])

    password = PasswordField('password', validators = [Required(), EqualTo('password_confirmation', message='Your passwords must match.')]) 
    password_confirmation = PasswordField('Confirm Password', validators = [Required()])

    submit = SubmitField("Register")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already in use.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first() or User.query.filter_by(username=field.data.lower()).first():
            raise ValidationError('Username already taken')
