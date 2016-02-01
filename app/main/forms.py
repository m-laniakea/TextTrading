from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Required, Email, Length

class LoginForm(Form):
    email = StringField('email@domain.com', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('password', validators=[Required()])
    submit = SubmitField('Log in')

