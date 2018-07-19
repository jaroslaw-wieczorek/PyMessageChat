from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):
    login = StringField('', validators=[DataRequired()])
    password = PasswordField('', validators=[DataRequired()])
    submit = SubmitField('Log in!')
