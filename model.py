from wtforms import StringField, SelectField, FileField, SelectMultipleField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Optional
from flask_wtf import FlaskForm
from datetime import datetime
from flask_login import UserMixin
from wtforms_alchemy.fields import QuerySelectField ,SelectMultipleField ,SelectField
from wtforms.validators import InputRequired, Email, Length , DataRequired ,Regexp , Optional

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

def state_choice():
    return db.session.query(State)

def country_choice():
    return db.session.query(Country)

def city_choice():
    return db.session.query(City)
    
class Firms(db.Model): 
    id = db.Column(db.Integer,  primary_key=True)
    firm_name = db.Column(db.String(50))
    firm_city = db.Column(db.String(50))
    firm_address_1 = db.Column(db.String(250))
    firm_pincode = db.Column(db.Integer())
    firm_country = db.Column(db.String(50))
    firm_state = db.Column(db.String(50))

class FirmForm(FlaskForm):
    firm_name = StringField('firm_name')
    firm_city = StringField('firm_city')
    firm_address_1 = StringField('firm_add_1')
    firm_pincode = StringField('firm_pincode')
    firm_country = StringField('firm_country')
    firm_state = StringField('firm_state')
    firm_submit = SubmitField('firm_submit')

#  Customer Category & Form

class CustomerCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    health = db.Column(db.String(5), unique=True, nullable=False)

class CustomerCategoryForm(FlaskForm):
    health = StringField('health', validators=[InputRequired()])
    health_submit = SubmitField('health_submit')
    health_update = SubmitField('health_update')


# State Model & Form

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(30), unique=True, nullable=False)
    
class StateForm(FlaskForm):
    state = StringField('state', validators=[InputRequired()])
    state_submit = SubmitField('state_submit')
    state_update = SubmitField('state_update')    

# Country Model & Form
    
class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(30), unique=True, nullable=False)

class CountryForm(FlaskForm):
    country = StringField('country', validators=[InputRequired()])
    country_submit = SubmitField('country_submit')
    country_update = SubmitField('country_update')    

# City Model & Form

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(30), unique=True, nullable=False)
    state = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(30), nullable=False)

class CityForm(FlaskForm):
    city = StringField('city', validators=[InputRequired()])
    state = QuerySelectField('state',validators=[InputRequired()] , query_factory=state_choice , allow_blank= False  , get_label='state')
    country = QuerySelectField('country', validators=[InputRequired()], query_factory=country_choice , allow_blank= False ,get_label='country')
    city_submit = SubmitField('city_submit')
    city_update = SubmitField('city_update')    

