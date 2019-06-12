from wtforms import StringField, SelectField, FileField, SelectMultipleField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Optional
from flask_wtf import FlaskForm
from datetime import datetime
from flask_login import UserMixin

from app import db

class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')


class SignupForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')
    email = StringField('email')


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer,  primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(250))