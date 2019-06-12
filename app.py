from flask import Flask, render_template, g, redirect, jsonify, url_for, request, session
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import logging

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from model import LoginForm, Users, SignupForm

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

logging.basicConfig(
    filename='trail.log',
    level=logging.DEBUG,
    format='[TRAIL] %(levelname)-7.7s %(message)s'
)


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    session['mssg'] = ""
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
            else:
                session['mssg'] = "Invalid Username or Password"
                return render_template('login.html', subtitle="Login", form=form, mssg=session['mssg'])
        else:
            session['mssg'] = "Invalid Username or Password"
            return render_template('login.html', subtitle="Login", form=form, mssg=session['mssg'])
    return render_template('login.html', subtitle="Login", form=form, mssg=session['mssg']), 200


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    session['mssg'] = ""
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pass = generate_password_hash(
                form.password.data, method='sha256')
            new_user = Users(username=form.username.data,
                             email=form.email.data, password=hashed_pass)
            # user_table = UserTableCreator(form.email.data)
            # Base.metadata.create_all(engine)
            db.session.add(new_user)
            db.session.commit()
            db.session.close()
            return redirect(url_for('login'))
        else:
            session['mssg'] = "Email ID already in use. Please login"

            return render_template('register.html', form=form, subtitle="Signup", mssg=session['mssg'])

    return render_template('register.html', subtitle="Signup", form=form, mssg=session['mssg']), 200


@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    return render_template('login.html', subtitle="Forgot"), 200


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('base.html' , subtitle="Home") , 200


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/message/session' , methods=['POST'])
@login_required
def mssg_del():
    session['mssg'] = ""
    return jsonify({'mssg' :'Emptying session mssg' })