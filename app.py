
from flask import Flask, render_template, g, redirect, jsonify, url_for, request, session
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import logging

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from model import Users , LoginForm , SignupForm , CustomerCategory , CustomerCategoryForm , City , State , Country ,\
    CityForm , StateForm , CountryForm , Firms , FirmForm , Uom , UomForm

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# logging.basicConfig(
#     filename='trail.log',
#     level=logging.DEBUG,
#     format='[TRAIL] %(levelname)-7.7s %(message)s'
# )


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                session['mssg'] = "Hey ! " + \
                    str(current_user.username) + " . Welcome."

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
            session['mssg'] = "You're all set. Please Login. "

            return redirect(url_for('login'))
        else:
            session['mssg'] = "Email ID already in use. Please login"

            return render_template('register.html', form=form, subtitle="Signup", mssg=session['mssg'])

    return render_template('register.html', subtitle="Signup", form=form, mssg=session['mssg']), 200


@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    return render_template('login.html', subtitle="Forgot", mssg=session['mssg']), 200


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    firm_form = FirmForm()
    firm_list = db.session.query(Firms).all()
    if firm_form.validate_on_submit():
        firm_name = str(firm_form.firm_name.data).title()
        check_one = db.session.query(Firms).filter_by(
            firm_name=firm_name).first()
        if check_one is None:
            new_firm = Firms(firm_name=firm_form.firm_name.data, firm_city=firm_form.firm_city.data, firm_address_1=firm_form.firm_address_1.data,
                             firm_state=firm_form.firm_state.data, firm_country=firm_form.firm_country.data, firm_pincode=firm_form.firm_pincode.data)
            db.session.add(new_firm)
            db.session.commit()
            session['mssg'] = "Firm '" + \
                str(firm_form.firm_name.data) + "' has been created."

            return redirect('/home')
        else:
            session['mssg'] = "Firm '" + \
                str(firm_form.firm_name.data) + "' already exists."
            return redirect('/home')
    return render_template('dash.html', subtitle="Home", mssg=session['mssg'], firm_form=firm_form, firm_list=firm_list), 200


@app.route('/basic_master', methods=['GET', 'POST'])
@login_required
def basic_master():

    # City Master

    city_list = db.session.query(
        City).all()
    city_form = CityForm()

    if city_form.validate_on_submit():
        if city_form.city_submit.data:

            city_name = str(city_form.city.data).title()
            check_one = City.query.filter_by(city=city_form.city.data).first()
            if check_one is not None:
                mssg = "City already exists "
                return redirect(url_for('basic_master'))

            else:
                print(city_form.state.data)
                state = city_form.state.data.state
                country = city_form.country.data.country
                new_city = City(city=city_name, state=state,
                                country=country)

                try:
                    db.session.add(new_city)
                    db.session.commit()
                    db.session.close()
                    session['mssg'] = "City - " + \
                        city_name+".  Successfully added"

                    return redirect(url_for('basic_master'))

                except Exception as e:
                    session['mssg'] = "Something went wrong"
                    return redirect(url_for('basic_master'))

    # State

    state_list = db.session.query(
        State).all()
    state_form = StateForm()

    if state_form.validate_on_submit():
        if state_form.state_submit.data:
            state_name = str(state_form.state.data).title()
            check_one = db.session.query(
                State).filter_by(state=state_name).first()
            if check_one is None:
                new_state = State(state=state_name)
                db.session.add(new_state)
                db.session.commit()
                return redirect('/basic_master')


    # Country

    country_list = db.session.query(
        Country).all()
    country_form = CountryForm()
    if country_form.validate_on_submit():
        if country_form.country_submit.data:
            country_name = str(country_form.country.data).title()
            check_one = db.session.query(
                Country).filter_by(country=country_name).first()
            if check_one is None:
                new_country = Country(country=country_name)
                db.session.add(new_country)
                db.session.commit()
                return redirect('/basic_master')


    cust_list = db.session.query(
        CustomerCategory).all()
    cust_form = CustomerCategoryForm()

    if cust_form.validate_on_submit():
        if cust_form.health_submit.data:
            cust_name = str(cust_form.health.data).title()
            check_one = db.session.query(
                CustomerCategory).filter_by(health=cust_name).first()
            if check_one is None:
                new_cust = CustomerCategory(health=cust_name)
                db.session.add(new_cust)
                db.session.commit()
                return redirect('/basic_master')

    
    
    uom_list = db.session.query(
        Uom).all()
    uom_form = UomForm()

    if uom_form.validate_on_submit():
        if uom_form.uom_submit.data:
            uom_name = str(uom_form.measure.data)
            check_one = db.session.query(
                Uom).filter_by(measure=uom_name).first()
            if check_one is None:
                new_uom = Uom(measure=uom_name , desc=  uom_form.desc.data , decimal = int(uom_form.decimal.data))
                db.session.add(new_uom)
                db.session.commit()
                return redirect('/basic_master')

    else:
        print(uom_form.errors)
    

    return render_template('basic_master.html', subtitle="Basic Master", mssg=session['mssg'], city_form=city_form, city_list=city_list,
                           state_form=state_form, state_list=state_list, country_form=country_form, country_list=country_list,
                           cust_list=cust_list,  cust_form= cust_form , uom_list=uom_list,  uom_form= uom_form), 200


# State Location Edits

@app.route("/basic_master/state/update/<id>", methods=['POST'])
@login_required
def state_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    state_form = StateForm()
    if state_form.state_update.data:
        state_name = str(state_form.state.data).title()
        check_one = db.session.query(
            State).filter_by(id=id).first()
        if check_one is not None:
            check_one.state = state_name
            db.session.commit()
            session['mssg'] = "State updated successfully"
            return redirect('/basic_master')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/basic_master')


@app.route("/basic_master/state/delete/<id>", methods=['POST', 'GET'])
@login_required
def state_delete(id):

    check_one = db.session.query(
        State).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "State deleted successfully"
        return redirect('/basic_master')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/basic_master')

# Country Location Edits


@app.route("/basic_master/country/update/<id>", methods=['POST'])
@login_required
def country_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    country_form = CountryForm()
    if country_form.country_update.data:
        country_name = str(country_form.country.data).title()
        check_one = db.session.query(
            Country).filter_by(id=id).first()
        if check_one is not None:
            check_one.country = country_name
            db.session.commit()
            session['mssg'] = "Country updated successfully"
            return redirect('/basic_master')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/basic_master')


@app.route("/basic_master/country/delete/<id>", methods=['POST', 'GET'])
@login_required
def country_delete(id):

    check_one = db.session.query(
        Country).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "Country deleted successfully"
        return redirect('/basic_master')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/basic_master')


# City Location Edit


@app.route("/basic_master/city/update/<id>", methods=['POST'])
@login_required
def city_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    city_form = CityForm()
    if city_form.city_update.data:
        city_name = str(city_form.city.data).title()
        check_one = db.session.query(
            City).filter_by(id=id).first()
        if check_one is not None:
            check_one.city = city_name
            check_one.state = city_form.state.data.state
            check_one.country = city_form.country.data.country
            db.session.commit()
            session['mssg'] = "City updated successfully"
            return redirect('/basic_master')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/basic_master')


@app.route("/basic_master/city/delete/<id>", methods=['POST', 'GET'])
@login_required
def city_delete(id):

    check_one = db.session.query(
        City).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "City deleted successfully"
        return redirect('/basic_master')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/basic_master')

# Health Location Edits

@app.route("/basic_master/health/update/<id>", methods=['POST'])
@login_required
def cust_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    cust_form = CustomerCategoryForm()
    if cust_form.health_update.data:
        cust_name = str(cust_form.health.data).title()
        check_one = db.session.query(
            CustomerCategory).filter_by(id=id).first()
        if check_one is not None:
            check_one.health = cust_name
            db.session.commit()
            session['mssg'] = "Customer Category updated successfully"
            return redirect('/basic_master')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/basic_master')


@app.route("/basic_master/health/delete/<id>", methods=['POST', 'GET'])
@login_required
def cust_delete(id):

    check_one = db.session.query(
        CustomerCategory).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "Customer Category deleted successfully"
        return redirect('/basic_master')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/basic_master')




# UOM  Edits

@app.route("/basic_master/uom/update/<id>", methods=['POST'])
@login_required
def uom_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    uom_form = UomForm()
    if uom_form.uom_update.data:
        uom_name = str(uom_form.measure.data)
        check_one = db.session.query(
            Uom).filter_by(id=id).first()
        if check_one is not None:
            check_one.measure = uom_name
            check_one.desc = uom_form.desc.data
            check_one.decimal = uom_form.decimal.data
            db.session.commit()
            session['mssg'] = "Measure updated successfully"
            return redirect('/basic_master')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/basic_master')


@app.route("/basic_master/uom/delete/<id>", methods=['POST', 'GET'])
@login_required
def uom_delete(id):

    check_one = db.session.query(
        Uom).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "Measure deleted successfully"
        return redirect('/basic_master')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/basic_master')


# Logout


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session['mssg'] = "You've been logged out."

    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/message/session', methods=['POST'])
@login_required
def mssg_del():
    session['mssg'] = None
    return jsonify({'mssg': 'Emptying session mssg'})


@app.route('/firm/delete/<firm>', methods=["POST", "GET"])
@login_required
def firm_delete(firm):
    try:
        firm_get = db.session.query(Firms).filter_by(id=int(firm)).first()
        firm_name = firm_get.firm_name
        db.session.query(Firms).filter_by(id=int(firm)).delete()
        db.session.commit()
        session["mssg"] = "Firm - "+str(firm_name)+" is deleted."
        return redirect('/')
    except Exception as e:
        logging.error('Error deleting Firm : ' + str(e))
        session["mssg"] = "Couldn't delete firm."
        return redirect('/')
