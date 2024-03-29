

from flask import Flask, render_template, g, redirect, jsonify, url_for, request, session
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import logging
import json
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
ma = Marshmallow(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from model import Users, LoginForm, SignupForm, CustomerCategory, CustomerCategoryForm, City, State, Country,\
    CityForm, StateForm, CountryForm, Firms, FirmForm, Uom, UomForm, Yarn, YarnForm, FabConst, FabConstForm, \
    FabProc, FabProcForm,  FabWidth, FabWidthForm, FabDye, FabDyeForm, RawCat, RawCatForm , FinCat , FinCatForm ,\
    FabComb , FabCombForm , PrintTech , PrintTechForm , FinDes , FinDesForm , FinSize , FinSizeForm , UnitLoc ,UnitLocForm

logging.basicConfig(
    filename='trail.log',
    level=logging.DEBUG,
    format='[TRAIL] %(levelname)-7.7s %(message)s'
)

from model import Role , UserForm

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                
                if user.roles[0].name == 'ADMIN' :
                    login_user(user)
                    session['mssg'] = "Hey ! " + \
                        str(current_user.username) + " . Welcome."

                    return redirect(url_for('home'))    
                
                elif user.roles[0].name == 'USER':
                    login_user(user)
                    session['mssg'] = "Hey ! " + \
                        str(current_user.username) + " . Welcome."

                    return redirect(url_for('user_home'))
            else:
                session['mssg'] = "Invalid Username or Password"
                return render_template('login.html', subtitle="Login", form=form, mssg=session['mssg'])
        else:
            session['mssg'] = "Invalid Username or Password"
            return render_template('login.html', subtitle="Login", form=form, mssg=session['mssg'])
    if not hasattr(session, "mssg"):
        session['mssg'] = ""
    
    if not hasattr(session , "dup"):
        session['dup'] = ""
    return render_template('login.html', subtitle="Login", form=form, mssg=session['mssg']), 200


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None:
            hashed_pass = generate_password_hash(
                form.password.data, method='sha256')
            new_user = Users(username=form.username.data,
                             password=hashed_pass)
            if str(form.email.data) == "jaitexart":
                check_role = db.session.query(Role).filter_by(name="ADMIN")
                if check_role.first() is None:
                    role = Role(name ="ADMIN")
                    db.session.add(role)
                    db.session.commit()
                    new_user.roles.append(role)
                else:
                    role = check_role.first()
                    new_user.roles.append(role)
                db.session.add(new_user)
                db.session.commit()
                db.session.close()
                session['mssg'] = "You're all set. Please Login. "

                return redirect(url_for('login'))
            elif str(form.email.data) == "user_ma":
                check_role = db.session.query(Role).filter_by(name="USER")
                if check_role.first() is None:
                    role = Role(name ="USER")
                    db.session.add(role)
                    db.session.commit()
                    new_user.roles.append(role)
                else:
                    role = check_role.first()
                    new_user.roles.append(role)
                    db.session.add(new_user)
                    db.session.commit()
                    db.session.close()
                    session['mssg'] = "You're all set. Please Login. "

                    return redirect(url_for('login'))
            else:
                session['mssg'] = "Not valid without key."
                return redirect(url_for('signup'))


           
        else:
            session['mssg'] = "User already in use. Please login"

            return render_template('register.html', form=form, subtitle="Signup", mssg=session['mssg'])

    return render_template('register.html', subtitle="Signup", form=form, mssg=session['mssg']), 200


@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    return render_template('login.html', subtitle="Forgot", mssg=session['mssg']), 200


@app.route('/user/home' , methods = ['GET' , 'POST'])
@login_required
def user_home():
    trans_list = db.session.query(Trans).filter( Trans.flag != 2).all()
    return render_template('dash_user.html' , trans_list = trans_list) , 200

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    trans_list = db.session.query(Trans).filter( Trans.flag != 2).all()
    return render_template('dash.html' , trans_list = trans_list) , 200



@app.route('/user/roles', methods=['GET', 'POST'])
@login_required
def user_roles():

    user_list = Users.query.all()
    form = UserForm()
    if form.validate_on_submit():
        if form.submit.data:
            user = Users.query.filter_by(username=form.username.data).first()
            if user is None:
                hashed_pass = generate_password_hash(
                    form.password.data, method='sha256')
                new_user = Users(username=form.username.data,
                                password=hashed_pass)
                role = Role.query.filter_by(name= 'USER').first()
                db.session.add(new_user)
                new_user.roles.append(role)
                db.session.commit()
                db.session.close()
                session['mssg'] = "You're all set. Please Login. "

                return redirect(url_for('user_roles'))
            else:
                session['mssg'] = "Username already in use. Please login"

                return redirect(url_for('user_roles'))

    return render_template('user_roles.html', subtitle="User Roles", mssg=session['mssg'], user_form=form , user_list = user_list), 200


# USER Roles Edit


# Raw MAterial Yarn  Edits

@app.route("/user-roles/update/<id>", methods=['POST'])
@login_required
def user_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    user_form = UserForm()
    if user_form.validate_on_submit():
        if user_form.update_submit.data:
            user_name = str(user_form.username.data)
            check_one = db.session.query(
                Users).filter_by(id=id).first()
            if check_one is not None:
                check_one.username = user_name
                db.session.commit()
                session['mssg'] = "User updated successfully"
                return redirect(url_for('user_roles'))
            else:
                session['mssg'] = "Something went wrong."
                return redirect(url_for('user_roles'))


@app.route("/user-roles/delete/<id>", methods=['POST', 'GET'])
@login_required
def user_delete(id):

    check_one = db.session.query(
        Users).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "User deleted successfully"
        return redirect(url_for('user_roles'))
    else:
        session['mssg'] = "Something went wrong."
        return redirect(url_for('user_roles'))


# Transaction Views 
# 
from model import Trans 

@app.route('/trans_a', methods=['GET', 'POST'])
@login_required
def trans_a():
    pp_num = db.session.query(Trans).all()
    trans_semi = db.session.query(Trans).filter_by(flag = 3).first()
    
    if len(pp_num) is 0:
        pp_new = int(1)
    else:
        pp_new = int(pp_num[-1].id) + 1

    if request.method == "POST":
        payload = json.dumps(request.json)
        payload = json.loads(payload)
        if 'pp_num' in payload :

            check_trans = db.session.query(Trans).filter_by(id= int(payload['pp_num'])).first()
            if check_trans is not None:
                check_trans.part_a = json.dumps(payload['data'])
                check_trans.flag = int(0)
                db.session.commit()
                session['mssg'] = "Transaction - Part A with PP No. " + str(check_trans.id )+ " has been updated."
                return jsonify("success")
        else:
            payload = json.dumps(request.json)
            new_trans = Trans(part_a = payload , part_b = "{}" )
            new_trans.flag = int(0)
            db.session.add(new_trans)
            db.session.commit()
            session['mssg'] = "Transaction - Part A with PP No. " + str(new_trans.id)+ " has been added."
            return jsonify("success")
    return render_template('trans_a.html' , pp_num = pp_new , mssg = session['mssg'] , trans_semi = trans_semi) ,200

@app.route('/trans_a_view', methods=['GET', 'POST'])
@login_required
def trans_a_view():
    pp_num = db.session.query(Trans).filter_by(flag= int(0)).all()

    return render_template('trans_a_view.html' , open_trans = pp_num , mssg = session['mssg']) , 200

import os

@app.route('/trans_a/uploads/<trans_id>' , methods= ['GET' , 'POST'])
@login_required
def trans_a_upload(trans_id):
    UPLOAD_FOLDER = os.path.abspath('./static/images/uploads/'+str(trans_id))
    
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
        try:
            filename = request.form['name']
            file = request.files['files[]']
            img_temp = os.path.join(UPLOAD_FOLDER,filename) 
            file.save(img_temp)
            return jsonify("success")
        except Exception as e:
            return jsonify("Error" + str(e))
    else:
        try:
            filename = request.form['name']
            file = request.files['files[]']
            img_temp = os.path.join(UPLOAD_FOLDER,filename) 
            file.save(img_temp)
            return jsonify("success")
        except Exception as e:
            return jsonify("Error" + str(e))

import urllib

@app.route('/trans_a_view/<trans_id>', methods=['GET', 'POST'])
@login_required
def trans_a_view_by_id(trans_id):
    pp_num = db.session.query(Trans).filter_by(id= int(trans_id)).all()
    trans_schema = TransSchema()
    res = trans_schema.dump(pp_num).data
    img_list = []
    UPLOAD_FOLDER = os.path.abspath('./static/images/uploads/'+str(trans_id))
    if not os.path.exists(UPLOAD_FOLDER):
        pass
    else:
        for r , d ,f in os.walk(UPLOAD_FOLDER):
            for file in f:
                img_list.append(str(trans_id)+'/'+str(file))

    return render_template('trans_a_view_id.html' , pp_num = trans_id , mssg = session['mssg'] , img_list = img_list) , 200

@app.route('/trans_a_user_view/<trans_id>', methods=['GET', 'POST'])
@login_required
def trans_a_user_view(trans_id):
    pp_num = db.session.query(Trans).filter_by(id= int(trans_id)).all()
    trans_schema = TransSchema()
    res = trans_schema.dump(pp_num).data
    img_list = []
    UPLOAD_FOLDER = os.path.abspath('./static/images/uploads/'+str(trans_id))
    if not os.path.exists(UPLOAD_FOLDER):
        pass
    else:
        for r , d ,f in os.walk(UPLOAD_FOLDER):
            for file in f:
                img_list.append(str(trans_id)+'/'+str(file))

    return render_template('trans_a_user_view.html' , pp_num = trans_id , mssg = session['mssg'] , img_list = img_list) , 200


from model import TransSchema

@app.route('/trans_a_view_data/<trans_id>' , methods = ['POST' , 'GET'])
@login_required
def trans_a_api(trans_id):
    pp_num = db.session.query(Trans).filter_by(id = int(trans_id)).first()
    trans_schema = TransSchema()
    res = trans_schema.dump(pp_num).data
    return jsonify({'trans_data': res})

@app.route('/trans_a_view_data/last' , methods = ['POST' , 'GET'])
@login_required
def trans_a_api_last():
    pp_num = db.session.query(Trans).filter( Trans.flag != int(2) ).all()[-1]
    trans_schema = TransSchema()
    res = trans_schema.dump(pp_num).data
    return jsonify({'trans_data': res})

@app.route('/trans_b/view/<trans_id>' , methods = ['POST' , 'GET'])
@login_required
def trans_b_view_by_id(trans_id):
    all_num = db.session.query(Trans).filter_by(flag = 0 ).all()

    pp_num = db.session.query(Trans).filter_by(id = int(trans_id)).first()
    view = 'true'
    return render_template('trans_b.html' ,open_trans = all_num , trans_num = pp_num.id , mssg = session['mssg'] , view = view) ,200


@app.route('/trans_b', methods=['GET', 'POST'])
@login_required
def trans_b():
    
    pp_num = db.session.query(Trans).filter_by(flag = 0 ).all()
    if request.method == "POST":
        try:
            payload = request.json
            pp_num = db.session.query(Trans).filter_by(id = int(payload['pp_num'])).first()
            update_obj = {}
            old_obj = json.loads(pp_num.part_b)
            new_obj = payload['data']
            update_obj["username"] = current_user.username
            update_obj["diff"] = json.dumps(diff(old_obj , new_obj , marshal = True) )
            update_obj["timestamp"] = str(moment.utcnow())
            dump = json.dumps(payload['data'])
            pp_num.part_b = dump  
            if len(pp_num.meta) is 0 :
                meta = []
                meta.append(update_obj)
                pp_num.meta = json.dumps(meta)
            else:
                temp_meta = json.loads(pp_num.meta)
                temp_meta.append(update_obj)
                pp_num.meta = json.dumps(temp_meta)
            db.session.commit()
            session['mssg'] = "Transaction - Part B with PP No. " + str( pp_num.id) + " updated."
            return jsonify("success")
        except Exception as e:
            logging.error(str(e))
    return render_template('trans_b.html' ,open_trans = pp_num , mssg = session['mssg']) ,200



# Transaction User Views 


@app.route('/trans_a_user', methods=['GET', 'POST'])
@login_required
def trans_a_user():
    pp_num = db.session.query(Trans).filter_by(flag= int(0)).all()

    return render_template('trans_a_user.html' , open_trans = pp_num , mssg = session['mssg']) , 200


from jsondiff import diff 
import moment

@app.route('/trans_b_user', methods=['GET', 'POST'])
@login_required
def trans_b_user():
    
    pp_num = db.session.query(Trans).filter_by(flag = 0 ).all()
    if request.method == "POST":
        payload = request.json
        pp_num = db.session.query(Trans).filter_by(id = int(payload['pp_num'])).first()
        update_obj = {}
        old_obj = json.loads(pp_num.part_b)
        new_obj = payload['data']
        update_obj["username"] = current_user.username
        update_obj["diff"] = diff(old_obj , new_obj)
        update_obj["timestamp"] = str(moment.utcnow())
        dump = json.dumps(payload['data'])
        pp_num.part_b = dump  
        if len(pp_num.meta) is 0 :
            meta = []
            meta.append(update_obj)
            pp_num.meta = json.dumps(meta)
        else:
            temp_meta = json.loads(pp_num.meta)
            temp_meta.append(update_obj)
            pp_num.meta = json.dumps(temp_meta)
        db.session.commit()
        session['mssg'] = "Transaction - Part B with PP No. " + str( pp_num.id) + " updated."
        return jsonify("success")
    return render_template('trans_b_user.html' ,open_trans = pp_num , mssg = session['mssg']) ,200

@app.route('/trans_b_user/view/<trans_id>' , methods = ['POST' , 'GET'])
@login_required
def trans_b_user_view(trans_id):
    all_num = db.session.query(Trans).filter_by(flag = 0 ).all()

    pp_num = db.session.query(Trans).filter_by(id = int(trans_id)).first()
    view = 'true'
    return render_template('trans_b_user.html' ,open_trans = all_num , trans_num = pp_num.id , mssg = session['mssg'] , view = view) ,200

# Entry dept Routes 
@app.route('/dept_entry/<dept>' ,methods = ['GET' , 'POST'])
@login_required
def dept_entry(dept):
    if current_user.roles[0].name == 'ADMIN' :
        return render_template('dept_entry.html' , dept = dept , mssg = session['mssg']) ,200
    elif current_user.roles[0].name == 'USER' :
        return render_template('dept_entry_user.html' , dept = dept , mssg = session['mssg']) ,200

# Basic Master Views
#
#

# Customer Category MAster


@app.route('/raw_materials/customer_category', methods=['GET', 'POST'])
@login_required
def customer_category():
    cust_list = db.session.query(
        CustomerCategory).all()
    cust_form = CustomerCategoryForm()

    if cust_form.validate_on_submit():
        if cust_form.health_submit.data:
            cust_name = str(cust_form.health.data).upper()
            check_one = db.session.query(
                CustomerCategory).filter_by(health=cust_name).first()
            if check_one is None:
                new_cust = CustomerCategory(health=cust_name)
                db.session.add(new_cust)
                db.session.commit()
                session['mssg'] = "Customer Category "+cust_name+" added successfully."
                return redirect(url_for('customer_category'))
            else:
                session['dup'] = check_one.health
                return redirect(url_for('customer_category'))

    return render_template('customer_category.html', subtitle="Customer Category", mssg=session['mssg'], dup=session['dup'], cust_form=cust_form), 200


@app.route('/raw_materials/customer_category_view', methods=['GET', 'POST'])
@login_required
def customer_category_view():
    cust_list = db.session.query(
        CustomerCategory).all()
    cust_form = CustomerCategoryForm()

    return render_template('customer_category_view.html', subtitle="Customer Category", mssg=session['mssg'], cust_list=cust_list, cust_form=cust_form), 200

from model import Accessories , AccessoriesForm

@app.route('/raw_materials/accessories', methods=['GET', 'POST'])
@login_required
def accessories():
    acc_list = db.session.query(
        Accessories).all()
    acc_form = AccessoriesForm()

    if acc_form.validate_on_submit():
        if acc_form.acc_submit.data:
            acc_name = str(acc_form.acc.data).lower()
            check_one = db.session.query(
                Accessories).filter_by(acc=acc_name).first()
            if check_one is None:
                new_acc = Accessories(acc=acc_name)
                new_acc.uom.append(acc_form.uom.data)
                db.session.add(new_acc)
                db.session.commit()
                session['mssg'] = "Accessory - "+acc_name+" has been added."
                return redirect(url_for('accessories'))
            else:
                session['mssg'] = "Accessory - "+acc_name+" already exists."
                session['dup'] = acc_name

                return redirect(url_for('accessories'))

    return render_template('accessories.html', subtitle="Accessories", mssg=session['mssg'], dup = session['dup'], acc_form=acc_form), 200


@app.route('/raw_materials/accessories_view', methods=['GET', 'POST'])
@login_required
def accessories_view():
    acc_list = db.session.query(
        Accessories).all()
    acc_form = AccessoriesForm()

    return render_template('accessories_view.html', subtitle="Accessories", mssg=session['mssg'],dup=session['dup'], acc_list=acc_list, acc_form=acc_form), 200



from model import OtherMat , OtherMatForm

@app.route('/raw_materials/OtherMat', methods=['GET', 'POST'])
@login_required
def other_mat():
    mat_list = db.session.query(
        OtherMat).all()
    mat_form = OtherMatForm()

    if mat_form.validate_on_submit():
        if mat_form.mat_submit.data:
            mat_name = str(mat_form.mat.data).lower()
            check_one = db.session.query(
                OtherMat).filter_by(mat=mat_name).first()
            if check_one is None:
                new_mat = OtherMat(mat=mat_name)
                new_mat.uom.append(mat_form.uom.data)

                db.session.add(new_mat)
                db.session.commit()
                session['mssg'] = "Material - "+mat_name+" has been added."
                return redirect(url_for('other_mat'))
            else:
                session['mssg'] = "Material - "+mat_name+" already exists."
                session['dup'] = mat_name
                return redirect(url_for('other_mat'))
    return render_template('othermat.html', subtitle="Other Materials", mssg=session['mssg'], dup = session['dup'] , mat_form=mat_form), 200


@app.route('/raw_materials/other_mat_view', methods=['GET', 'POST'])
@login_required
def other_mat_view():
    mat_list = db.session.query(
        OtherMat).all()
    mat_form = OtherMatForm()

    return render_template('othermat_view.html', subtitle="Other Materials", mssg=session['mssg'], mat_list=mat_list, mat_form=mat_form), 200


@app.route('/unit_location', methods=['GET', 'POST'])
@login_required
def unit_loc():
    unit_list = db.session.query(
        UnitLoc).all()
    unit_form = UnitLocForm()

    if unit_form.validate_on_submit():
        if unit_form.unit_submit.data:
            unit_name = str(unit_form.unit.data).lower()
            check_one = db.session.query(
                UnitLoc).filter_by(unit=unit_name).first()
            if check_one is None:
                new_unit = UnitLoc(unit=unit_name)
                db.session.add(new_unit)
                db.session.commit()
                session['mssg'] = "Unit Location "+unit_name+" added successfully."
                return redirect(url_for('unit_loc'))
            else:
                session['dup'] = check_one.unit
                return redirect(url_for('unit_loc'))

    return render_template('unit_location.html', subtitle="Unit Location", mssg=session['mssg'], dup=session['dup'],unit_list = unit_list, unit_form=unit_form), 200




# UOM Master


@app.route('/raw_materials/uom', methods=['GET', 'POST'])
@login_required
def uom():
    uom_list = db.session.query(
        Uom).all()
    uom_form = UomForm()

    if uom_form.validate_on_submit():
        if uom_form.uom_submit.data:
            uom_name = str(uom_form.measure.data).lower()
            check_one = db.session.query(
                Uom).filter_by(measure=uom_name).first()
            if check_one is None:
                new_uom = Uom(measure=uom_name, desc=uom_form.desc.data,
                              decimal=int(uom_form.decimal.data))
                db.session.add(new_uom)
                db.session.commit()
                session['mssg'] = "Measure - "+uom_name+" has been added."
                return redirect(url_for('uom'))
            else:
                session['mssg'] = "Measure - "+uom_name+" already exists."
                session['dup'] = uom_name
                return redirect(url_for('uom'))
    return render_template('uom_master.html', subtitle="Unit of Measurement", mssg=session['mssg'],dup = session['dup'] ,uom_form=uom_form), 200


# Location Master


@app.route('/raw_materials/location', methods=['GET', 'POST'])
@login_required
def location():
    city_list = db.session.query(
        City).all()
    city_form = CityForm()

    if city_form.validate_on_submit():
        if city_form.city_submit.data:

            city_name = str(city_form.city.data).title()
            check_one = City.query.filter_by(city=city_form.city.data).first()
            if check_one is not None:
                session['mssg'] = "City already exists "
                return redirect(url_for('location'))

            else:
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

                    return redirect(url_for('location'))

                except Exception as e:
                    session['mssg'] = "Something went wrong"
                    return redirect(url_for('location'))

    # State

    state_list = db.session.query(
        State).all()
    state_form = StateForm()

    if state_form.validate_on_submit():
        if state_form.state_submit.data:
            state_name = str(state_form.state.data).title()
            check_one = db.session.query(
                State).filter_by(state=state_name).first()
            if check_one is not None:
                session['mssg'] = "State already exists "
            else:
                new_state = State(state=state_name)
                db.session.add(new_state)
                db.session.commit()
                session['mssg'] = "State - "+state_name+" successfully added. "
                return redirect('/location')

    # Country

    country_list = db.session.query(
        Country).all()
    country_form = CountryForm()
    if country_form.validate_on_submit():
        if country_form.country_submit.data:
            country_name = str(country_form.country.data).title()
            check_one = db.session.query(
                Country).filter_by(country=country_name).first()
            if check_one is not None:
                session['mssg'] = "Country already exists "
            else:
                new_country = Country(country=country_name)
                db.session.add(new_country)
                db.session.commit()
                session['mssg'] = "Country - "+country_name+" successfully added. "
                return redirect('/location')    
    
    return render_template('location_master.html', subtitle="Location", mssg=session['mssg'], city_form=city_form, city_list=city_list,
                           state_form=state_form, state_list=state_list, country_form=country_form, country_list=country_list), 200

@app.route('/raw_materials/uom_view', methods=['GET', 'POST'])
@login_required
def uom_master_view():
    uom_list = db.session.query(
        Uom).all()
    uom_form = UomForm()

    return render_template('uom_master_view.html', subtitle="Unit of Measurement", mssg=session['mssg'], uom_list=uom_list, uom_form=uom_form), 200

@app.route('/finished_goods', methods=['GET', 'POST'])
@login_required
def fin_goods():
    
    cat_list = db.session.query(
        FinCat).all()
    cat_form = FinCatForm()

    if cat_form.validate_on_submit():
        if cat_form.cat_submit.data:
            cat_name = str(cat_form.cat.data).lower()
            check_one = db.session.query(
                FinCat).filter_by(cat=cat_name).first()
            if check_one is not None:
                session['mssg'] = "Fabric Category already exists "
                session['dup'] = check_one.cat

            else:
                new_cat = FinCat(
                    cat=cat_name, desc=cat_form.desc.data)
                db.session.add(new_cat)
                db.session.commit()
                session['mssg'] = "Fabric Category - " + \
                    cat_name+"  successfully added."
            return redirect('/finished_goods?showTab=1')

    comb_list = db.session.query(
        FabComb).all()
    comb_form = FabCombForm()

    if comb_form.validate_on_submit():
        if comb_form.comb_submit.data:
            comb_name = str(comb_form.comb.data).lower()
            check_one = db.session.query(
                FabComb).filter_by(comb=comb_name).first()
            if check_one is not None:
                session['mssg'] = "Fabric Combination already exists "
                session['dup'] = check_one.comb

            else:
                new_comb = FabComb(
                    comb=comb_name, top_desc=comb_form.top_desc.data, dup_desc=comb_form.dup_desc.data
                    , sal_desc=comb_form.sal_desc.data, fab_desc=comb_form.fab_desc.data)
                db.session.add(new_comb)
                db.session.commit()
                session['mssg'] = "Fabric Combination - " + \
                    comb_name+"  successfully added."
            return redirect('/finished_goods?showTab=2')
    
    tech_list = db.session.query(
        PrintTech).all()
    tech_form = PrintTechForm()

    if tech_form.validate_on_submit():
        if tech_form.tech_submit.data:
            tech_name = str(tech_form.tech.data).lower()
            check_one = db.session.query(
                PrintTech).filter_by(tech=tech_name).first()
            if check_one is not None:
                session['mssg'] = "Print Technique already exists "
                session['dup'] = tech_name

            else:
                new_tech = PrintTech(
                    tech=tech_name, desc=tech_form.desc.data)
                db.session.add(new_tech)
                db.session.commit()
                session['mssg'] = "Print Technique - " + \
                    tech_name+"  successfully added."
            return redirect('/finished_goods?showTab=3')

    des_list = db.session.query(
        FinDes).all()
    des_form = FinDesForm()

    if des_form.validate_on_submit():
        if des_form.des_submit.data:
            des_name = str(des_form.des.data)
            check_one = db.session.query(
                FinDes).filter_by(des=des_name).first()
            if check_one is not None:
                session['mssg'] = "Design already exists "
                session['dup'] = des_name

            else:
                new_des = FinDes(des=des_name)
                db.session.add(new_des)
                db.session.commit()
                session['mssg'] = "Design - " + \
                    des_name+" successfully added."
            return redirect('/finished_goods?showTab=4')
    
    size_list = db.session.query(
        FinSize).all()
    size_form = FinSizeForm()

    if size_form.validate_on_submit():
        if size_form.size_submit.data:
            size_name = str(size_form.size.data).upper()
            check_one = db.session.query(
                FinSize).filter_by(size=size_name).first()
            if check_one is not None:
                session['mssg'] = "Size already exists "
                session['dup'] = size_name
            else:
                new_size = FinSize(size=size_name)
                db.session.add(new_size)
                db.session.commit()
                session['mssg'] = "Size - " + \
                    size_name+" successfully added."
            return redirect('/finished_goods?showTab=5')

    return render_template('fin_goods.html' , subtitle = "Finished Goods " , mssg = session['mssg'] , dup= session['dup'], cat_list =cat_list ,cat_form = cat_form ,\
         comb_list =comb_list ,comb_form = comb_form , tech_list = tech_list , tech_form = tech_form , des_list = des_list ,des_form = des_form ,\
             size_list = size_list , size_form = size_form)


# FInished Good Edits

@app.route("/finished_goods/cate/update/<id>", methods=['POST'])
@login_required
def pcat_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    cat_form = FinCatForm()
    if cat_form.cat_update.data:
        cat_name = str(cat_form.cat.data).lower()
        check_one = db.session.query(
            FinCat).filter_by(id=id).first()
        if check_one is not None:
            check_one.cat = cat_name
            check_one.desc = cat_form.desc.data
            db.session.commit()
            session['mssg'] = "Finished Goods Category updated successfully"
            return redirect('/finished_goods?showTab=1&view=list')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/finished_goods?showTab=1&view=list')


@app.route("/finished_goods/cat/delete/<id>", methods=['POST', 'GET'])
@login_required
def pcat_delete(id):

    check_one = db.session.query(
        FinCat).filter_by(id=id)
    if check_one.first() is not None:
        if len(check_one.first().cat_goods) is int(0):
            check_one.delete()
            db.session.commit()
            session['mssg'] = "Category deleted successfully"
            return redirect('/finished_goods?showTab=1&view=list')
        else:
            session['mssg'] = "Cannot delete. Value is being used."
            return redirect('/finished_goods?showTab=1&view=list')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/finished_goods?showTab=1&view=list')

# FInished Comb Edits

@app.route("/finished_goods/comb/update/<id>", methods=['POST'])
@login_required
def comb_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    comb_form = FabCombForm()
    if comb_form.comb_update.data:
        comb_name = str(comb_form.comb.data).lower()
        check_one = db.session.query(
            FabComb).filter_by(id=id).first()
        if check_one is not None:
            check_one.comb = comb_name
            check_one.top_desc = comb_form.top_desc.data
            check_one.dup_desc = comb_form.dup_desc.data
            check_one.sal_desc = comb_form.sal_desc.data
            check_one.fab_desc = comb_form.fab_desc.data

            db.session.commit()
            session['mssg'] = "Finished Goods Combination updated successfully"
            return redirect('/finished_goods?showTab=2&view=list')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/finished_goods?showTab=2&view=list')


@app.route("/finished_goods/comb/delete/<id>", methods=['POST', 'GET'])
@login_required
def comb_delete(id):

    check_one = db.session.query(
        FabComb).filter_by(id=id)
    if check_one.first() is not None:
        if len(check_one.first().comb_goods) is int(0):
            check_one.delete()
            db.session.commit()
            session['mssg'] = "Combination deleted successfully"
            return redirect('/finished_goods?showTab=2&view=list')
        else:
            session['mssg'] = "Cannot delete. Value is being used."
            return redirect('/finished_goods?showTab=2&view=list')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/finished_goods?showTab=2&view=list')

# FInished Tech Edits

@app.route("/finished_goods/technique/update/<id>", methods=['POST'])
@login_required
def tech_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    tech_form = PrintTechForm()
    if tech_form.tech_update.data:
        tech_name = str(tech_form.tech.data).lower()
        check_one = db.session.query(
            PrintTech).filter_by(id=id).first()
        if check_one is not None:
            check_one.tech = tech_name
            check_one.desc = tech_form.desc.data
            db.session.commit()
            session['mssg'] = "Print Technique updated successfully"
            return redirect('/finished_goods?showTab=3&view=list')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/finished_goods?showTab=3&view=list')


@app.route("/finished_goods/tech/delete/<id>", methods=['POST', 'GET'])
@login_required
def tech_delete(id):

    check_one = db.session.query(
        PrintTech).filter_by(id=id)
    if check_one.first() is not None:
        if len(check_one.first().print_goods) is int(0):
            check_one.delete()
            db.session.commit()
            session['mssg'] = "Print Technique deleted successfully"
            return redirect('/finished_goods?showTab=3&view=list')
        else:
            session['mssg'] = "Cannot delete. Value is being used."
            return redirect('/finished_goods?showTab=3&view=list')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/finished_goods?showTab=3&view=list')


# FInished Des Edits

@app.route("/finished_goods/design/update/<id>", methods=['POST'])
@login_required
def des_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    des_form = FinDesForm()
    if des_form.des_update.data:
        des_name = str(des_form.des.data).lower()
        check_one = db.session.query(
            FinDes).filter_by(id=id).first()
        if check_one is not None:
            check_one.des = des_name
            db.session.commit()
            session['mssg'] = "Fabric Design updated successfully"
            return redirect('/finished_goods?showTab=4&view=list')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/finished_goods?showTab=4&view=list')


@app.route("/finished_goods/des/delete/<id>", methods=['POST', 'GET'])
@login_required
def des_delete(id):

    check_one = db.session.query(
        FinDes).filter_by(id=id)
    if check_one.first() is not None:
        if len(check_one.first().des_goods) is int(0):        
            check_one.delete()
            db.session.commit()
            session['mssg'] = "Fabric Design deleted successfully"
            return redirect('/finished_goods?showTab=4&view=list')
        else:
            session['mssg'] = "Cannot delete. Value is being used."
            return redirect('/finished_goods?showTab=4&view=list')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/finished_goods?showTab=4&view=list')

# Finished Des Edits

@app.route("/finished_goods/size/update/<id>", methods=['POST'])
@login_required
def size_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    size_form = FinSizeForm()
    if size_form.size_update.data:
        size_name = str(size_form.size.data).upper()
        check_one = db.session.query(
            FinSize).filter_by(id=id).first()
        if check_one is not None:
            check_one.size = size_name.upper()
            db.session.commit()
            session['mssg'] = "Fabric Size updated successfully"
            return redirect('/finished_goods?showTab=5&view=list')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/finished_goods?showTab=5&view=list')


@app.route("/finished_goods/size/delete/<id>", methods=['POST', 'GET'])
@login_required
def size_delete(id):

    check_one = db.session.query(
        FinSize).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "Fabric Size deleted successfully"
        return redirect('/finished_goods?showTab=5&view=list')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/finished_goods?showTab=5&view=list')



@app.route('/firms', methods=['GET', 'POST'])
@login_required
def firms():
    firm_form = FirmForm()
    firm_list = db.session.query(Firms).all()
    if firm_form.validate_on_submit():
        firm_name = str(firm_form.firm_name.data).lower()
        check_one = db.session.query(Firms).filter_by(
            firm_name=firm_name).first()
        if check_one is None:
            new_firm = Firms(firm_name=firm_form.firm_name.data, firm_city=firm_form.firm_city.data, firm_address_1=firm_form.firm_address_1.data,
                             firm_state=firm_form.firm_state.data, firm_country=firm_form.firm_country.data, firm_pincode=firm_form.firm_pincode.data)
            db.session.add(new_firm)
            db.session.commit()
            session['mssg'] = "Firm '" + \
                str(firm_form.firm_name.data) + "' has been created."

            return redirect('/firms')
        else:
            session['mssg'] = "Firm '" + \
                str(firm_form.firm_name.data) + "' already exists."
            return redirect('/firms')
    return render_template('firms.html', subtitle="Home", mssg=session['mssg'], firm_form=firm_form, firm_list=firm_list), 200


from model import FinGoodsForm , RawFabMainForm , FinGoods ,RawFabMain

@app.route('/main_master/', defaults = {'fin_id' : None} , methods=['GET', 'POST'])
@app.route('/main_master/<fin_id>' , methods=['POST'])
@login_required
def main_master(fin_id):
    fin_goods_form = FinGoodsForm()

    raw_goods_form = RawFabMainForm()

    raw_goods = RawFabMain()
    fin_goods = FinGoods.query.all()
    raw_goods = RawFabMain.query.all()
    
    if fin_goods_form.fin_submit.data :
        new_fin_good = FinGoods(alt_name = str(fin_goods_form.alt_name.data).lower())
        try:
            # if(fin_goods_form.product_category.data not in fin_good.product_category and .... )
            #  Then procedd with addition 
            db.session.add(new_fin_good)

            new_fin_good.product_category.append(fin_goods_form.product_category.data)
            new_fin_good.fabric_combo.append(fin_goods_form.fabric_combo.data)
            new_fin_good.print_tech.append(fin_goods_form.print_tech.data)
            new_fin_good.design.append(fin_goods_form.design.data)
            new_fin_good.uom.append(fin_goods_form.uom.data)
            db.session.commit()
            db.session.close()
            session['mssg'] = "Finished Goods successfully added."
            return redirect('/main_master?showTab=14')
        except Exception as e:
            session['mssg'] = "Something unexpected happened."
            logging.error(str(e))
            return redirect('/main_master?showTab=14')
    
    if fin_goods_form.fin_update.data:
        try:
            fin_g_id = int(fin_id)
            db.session.query(FinGoods).filter_by(id = fin_g_id).delete()
            new_fin_good = FinGoods(alt_name = str(fin_goods_form.alt_name.data).lower())

            new_fin_good.product_category.append(fin_goods_form.product_category.data)
            
            new_fin_good.fabric_combo.append(fin_goods_form.fabric_combo.data)
          
            new_fin_good.print_tech.append(fin_goods_form.print_tech.data)

       
            new_fin_good.design.append(fin_goods_form.design.data)

            new_fin_good.uom.append(fin_goods_form.uom.data)
            session["mssg"] = "Finished Goods has been updated."

            db.session.commit()
            return redirect('/main_master?showTab=14&view=list')
        except Exception as e:
            session['mssg'] = "Something unexpected happened."
            logging.error(str(e))
            return redirect('/main_master?showTab=14&view=list')
    

    if raw_goods_form.raw_submit.data :
        new_raw_good = RawFabMain(alt_name = str(raw_goods_form.alt_name.data).lower())
        try:
            db.session.add(new_raw_good)
            new_raw_good.product_category.append(raw_goods_form.product_category.data)
            new_raw_good.yarn.append(raw_goods_form.yarn.data)
            new_raw_good.fab_const.append(raw_goods_form.fab_const.data)
            new_raw_good.proc.append(raw_goods_form.proc.data)
            new_raw_good.uom.append(raw_goods_form.uom.data)
            new_raw_good.width.append(raw_goods_form.width.data)
            new_raw_good.dye.append(raw_goods_form.dye.data)

            db.session.commit()
            db.session.close()
            session['mssg'] = "Raw Material Fabric successfully added."
            return redirect('/main_master?showTab=15')
        except Exception as e:
            session['mssg'] = "Something unexpected happened."
            return redirect('/main_master?showTab=15')
    
    if raw_goods_form.raw_update.data:
        try:
            raw_g_id = int(fin_id)
            db.session.query(RawFabMain).filter_by(id = raw_g_id).delete()
            new_raw_good = RawFabMain(alt_name = str(raw_goods_form.alt_name.data).lower())

            new_raw_good.product_category.append(raw_goods_form.product_category.data)
            new_raw_good.yarn.append(raw_goods_form.yarn.data)
            new_raw_good.fab_const.append(raw_goods_form.fab_const.data)
            new_raw_good.proc.append(raw_goods_form.proc.data)
            new_raw_good.uom.append(raw_goods_form.uom.data)
            new_raw_good.width.append(raw_goods_form.width.data)
            new_raw_good.dye.append(raw_goods_form.dye.data)

            db.session.commit()
            db.session.close()
            session['mssg'] = "Raw Material Fabric successfully added."
            return redirect('/main_master?showTab=15&view=list')
        except Exception as e:
            session['mssg'] = "Something unexpected happened."
            logging.error(str(e))
            return redirect('/main_master?showTab=15&view=list')

    return render_template('main_master.html' ,mssg=session['mssg'], fin_form = fin_goods_form , raw_form = raw_goods_form , fin_goods_list = fin_goods , raw_goods_list = raw_goods ) ,200


@app.route('/raw_materials', methods=['GET', 'POST'])
@login_required
def raw_materials():
 

    # Yarn Form

    yarn_list = db.session.query(
        Yarn).all()
    yarn_form = YarnForm()

    if yarn_form.validate_on_submit():
        if yarn_form.yarn_submit.data:
            yarn_name = str(yarn_form.yarn.data).lower()
            check_one = db.session.query(
                Yarn).filter_by(yarn=yarn_name).first()
            if check_one is not None:
                session['mssg'] = "Yarn already exists "
                session['dup'] = yarn_name
            else:
                new_yarn = Yarn(yarn=yarn_name, desc=yarn_form.desc.data)
                db.session.add(new_yarn)
                db.session.commit()
                session['mssg'] = "Yarn - "+yarn_name+" successfully added."
            return redirect('/raw_materials?showTab=8')

    # Fabric Construction Form

    const_list = db.session.query(
        FabConst).all()
    const_form = FabConstForm()

    if const_form.validate_on_submit():
        if const_form.const_submit.data:
            const_name = str(const_form.const.data).lower()
            check_one = db.session.query(
                FabConst).filter_by(const=const_name).first()
            if check_one is not None:
                session['mssg'] = "Construction already exists "
                session['dup'] = const_name

            else:
                new_const = FabConst(const=const_name)
                db.session.add(new_const)
                db.session.commit()
                session['mssg'] = "Construction - " + \
                    const_name+" successfully added."
            return redirect('/raw_materials?showTab=13')

    # Fabric process Form

    process_list = db.session.query(
        FabProc).all()
    process_form = FabProcForm()

    if process_form.validate_on_submit():
        if process_form.proc_submit.data:
            process_name = str(process_form.proc.data).lower()
            check_one = db.session.query(
                FabProc).filter_by(process=process_name).first()
            if check_one is not None:
                session['mssg'] = "Fabric Process already exists "  
                session['dup'] = process_name
            else:
                new_process = FabProc(
                    process=process_name, desc=process_form.desc.data)
                db.session.add(new_process)
                db.session.commit()
                session['mssg'] = "Fabric Process - " + \
                    process_name+"  successfully added."
            return redirect('/raw_materials?showTab=9')

    # Fabric Width Form

    width_list = db.session.query(
        FabWidth).all()
    width_form = FabWidthForm()

    if width_form.validate_on_submit():
        if width_form.width_submit.data:
            width_name = str(width_form.width.data).lower()
            check_one = db.session.query(
                FabWidth).filter_by(width=width_name).first()
            if check_one is not None:
                session['mssg'] = "Fabric Width already exists "
                session['dup'] = width_name
            else:
                new_width = FabWidth(width=width_name)
                db.session.add(new_width)
                db.session.commit()
                session['mssg'] = "Fabric Width - " + \
                    width_name+"  successfully added."
            return redirect('/raw_materials?showTab=10')

    # Fabric Dye Form

    dye_list = db.session.query(
        FabDye).all()
    dye_form = FabDyeForm()

    if dye_form.validate_on_submit():
        if dye_form.dye_submit.data:
            dye_name = str(dye_form.dye.data).lower()
            check_one = db.session.query(
                FabDye).filter_by(dye=dye_name).first()
            if check_one is not None:
                session['mssg'] = "Fabric Dye already exists "
                session['dup'] = dye_name
            else:
                new_dye = FabDye(dye=dye_name)
                db.session.add(new_dye)
                db.session.commit()
                session['mssg'] = "Fabric Dye - " + \
                    dye_name+"  successfully added."
            return redirect('/raw_materials?showTab=11')

    # Raw Mat Cateogry Form

    cat_list = db.session.query(
        RawCat).all()
    cat_form = RawCatForm()

    if cat_form.validate_on_submit():
        if cat_form.cat_submit.data:
            cat_name = str(cat_form.cat.data).lower()
            check_one = db.session.query(
                RawCat).filter_by(cat=cat_name).first()
            if check_one is not None:
                session['mssg'] = "Raw Material Category already exists "
                session['dup'] = cat_name
            else:
                new_cat = RawCat(cat=cat_name, desc=cat_form.desc.data)
                db.session.add(new_cat)
                db.session.commit()
                session['mssg'] = "Category - " + \
                    cat_name+"  successfully added."
            return redirect('/raw_materials?showTab=12')

    return render_template('raw_mat_master.html', subtitle="Basic Master", mssg=session['mssg'], dup = session['dup'] ,
                           yarn_list=yarn_list,  yarn_form=yarn_form,  const_list=const_list, const_form=const_form,
                           width_list=width_list, width_form=width_form,  process_list=process_list, process_form=process_form,
                           dye_list=dye_list, dye_form=dye_form, cat_list=cat_list, cat_form=cat_form), 200




# State Location Edits

@app.route("/raw_materials/state/update/<id>", methods=['POST'])
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
            return redirect('/raw_materials')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/raw_materials')


@app.route("/raw_materials/state/delete/<id>", methods=['POST', 'GET'])
@login_required
def state_delete(id):

    check_one = db.session.query(
        State).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "State deleted successfully"
        return redirect('/raw_materials')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/raw_materials')

# Country Location Edits


@app.route("/raw_materials/country/update/<id>", methods=['POST'])
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
            return redirect('/raw_materials')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/raw_materials')


@app.route("/raw_materials/country/delete/<id>", methods=['POST', 'GET'])
@login_required
def country_delete(id):

    check_one = db.session.query(
        Country).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "Country deleted successfully"
        return redirect('/raw_materials')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/raw_materials')


# City Location Edit


@app.route("/raw_materials/city/update/<id>", methods=['POST'])
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
            return redirect('/raw_materials')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/raw_materials')


@app.route("/raw_materials/city/delete/<id>", methods=['POST', 'GET'])
@login_required
def city_delete(id):

    check_one = db.session.query(
        City).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "City deleted successfully"
        return redirect('/raw_materials')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/raw_materials')

# Health Location Edits


@app.route("/raw_materials/health/update/<id>", methods=['POST'])
@login_required
def cust_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    cust_form = CustomerCategoryForm()
    if cust_form.health_update.data:
        cust_name = str(cust_form.health.data).upper()
        check_one = db.session.query(
            CustomerCategory).filter_by(id=id).first()
        if check_one is not None:
            check_one.health = cust_name
            db.session.commit()
            session['mssg'] = "Customer Category updated successfully"
            return redirect('/raw_materials/customer_category_view')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/raw_materials/customer_category_view')


@app.route("/raw_materials/health/delete/<id>", methods=['POST', 'GET'])
@login_required
def cust_delete(id):

    check_one = db.session.query(
        CustomerCategory).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "Customer Category deleted successfully"
        return redirect('/raw_materials/customer_category_view')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/raw_materials/customer_category_view')

# Unit Location Edits


@app.route("/unit/update/<id>", methods=['POST'])
@login_required
def unit_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    unit_form = UnitLocForm()
    if unit_form.unit_update.data:
        unit_name = str(unit_form.unit.data).lower()
        check_one = db.session.query(
            UnitLoc).filter_by(id=id).first()
        if check_one is not None:
            check_one.unit = unit_name
            db.session.commit()
            session['mssg'] = "Unit Location updated successfully"
            return redirect('/unit_location?view=list')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/unit_location?view=list')


@app.route("/unit/delete/<id>", methods=['POST', 'GET'])
@login_required
def unit_delete(id):

    check_one = db.session.query(
        UnitLoc).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "Unit Location deleted successfully"
        return redirect('/unit_location?view=list')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/unit_location?view=list')

# Accessories  Edits


@app.route("/raw_materials/acc/update/<id>", methods=['POST'])
@login_required
def acc_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    acc_form = AccessoriesForm()
    if acc_form.acc_update.data:
        acc_name = str(acc_form.acc.data).lower()
        check_one = db.session.query(
            Accessories).filter_by(id=id)
        if check_one.first() is not None:
            check_one.delete()
            new_acc = Accessories(acc = acc_name)
            new_acc.uom.append(acc_form.uom.data)
            db.session.commit()
            session['mssg'] = "Accessories updated successfully"
            return redirect('/raw_materials/accessories_view')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/raw_materials/accessories_view')


@app.route("/raw_materials/acc/delete/<id>", methods=['POST', 'GET'])
@login_required
def acc_delete(id):

    check_one = db.session.query(
        Accessories).filter_by(id=id)
    if check_one.first() is not None:
        session['mssg'] = "Accessories - "+ check_one.first().acc +" deleted successfully"
        check_one.delete()
        db.session.commit()
        return redirect('/raw_materials/accessories_view')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/raw_materials/accessories_view')


# Other Materials  Edits


@app.route("/raw_materials/mat/update/<id>", methods=['POST'])
@login_required
def mat_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    mat_form = OtherMatForm()
    if mat_form.mat_update.data:
        mat_name = str(mat_form.mat.data).lower()
        check_one = db.session.query(
            OtherMat).filter_by(id=id)
        if check_one.first() is not None:
            check_one.delete()
            new_mat = OtherMat(mat = mat_name)
            new_mat.uom.append(mat_form.uom.data)
            db.session.commit()
            session['mssg'] = "Accessories updated successfully"
            return redirect('/raw_materials/other_mat_view')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/raw_materials/other_mat_view')


@app.route("/raw_materials/mat/delete/<id>", methods=['POST', 'GET'])
@login_required
def mat_delete(id):

    check_one = db.session.query(
        OtherMat).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "Other Materials deleted successfully"
        return redirect('/raw_materials/other_mat_view')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/raw_materials/other_mat_view')

# UOM  Edits

@app.route("/raw_materials/uom/update/<id>", methods=['POST'])
@login_required
def uom_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    uom_form = UomForm()
    if uom_form.uom_update.data:
        uom_name = str(uom_form.measure.data).lower()
        check_one = db.session.query(
            Uom).filter_by(id=id).first()
        if check_one is not None:
            check_one.measure = uom_name
            check_one.desc = uom_form.desc.data
            check_one.decimal = uom_form.decimal.data
            db.session.commit()
            session['mssg'] = "Measure updated successfully"
            return redirect('/raw_materials/uom_view')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/raw_materials/uom_view')


@app.route("/raw_materials/uom/delete/<id>", methods=['POST', 'GET'])
@login_required
def uom_delete(id):

    check_one = db.session.query(
        Uom).filter_by(id=id)
    if check_one.first() is not None:
        if len(check_one.first().uom_goods) is int(0) and len(check_one.first().uom_raw_goods) is int(0):
            check_one.delete()
            db.session.commit()
            session['mssg'] = "Measure deleted successfully"
            return redirect('/raw_materials/uom_view')
        else:
            session['mssg'] = "Cannot delete. Value is being used."
            return redirect('/raw_materials/uom_view')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/raw_materials/uom_view')


# Raw MAterial Yarn  Edits

@app.route("/raw_materials/yarn/update/<id>", methods=['POST'])
@login_required
def yarn_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    yarn_form = YarnForm()
    if yarn_form.yarn_update.data:
        yarn_name = str(yarn_form.yarn.data).lower()
        check_one = db.session.query(
            Yarn).filter_by(id=id).first()
        if check_one is not None:
            check_one.yarn = yarn_name
            check_one.desc = yarn_form.desc.data
            db.session.commit()
            session['mssg'] = "Yarn updated successfully"
            return redirect('/raw_materials?showTab=8&view=list')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/raw_materials?showTab=8&view=list')


@app.route("/raw_materials/yarn/delete/<id>", methods=['POST', 'GET'])
@login_required
def yarn_delete(id):

    check_one = db.session.query(
        Yarn).filter_by(id=id)
    if check_one.first() is not None:
        if len(check_one.first().yarn_goods) is int(0):
            check_one.delete()
            db.session.commit()
            session['mssg'] = "Yarn deleted successfully"
            return redirect('/raw_materials?showTab=8&view=list')
        else:
            session['mssg'] = "Cannot delete. Value is being used."
            return redirect('/raw_materials?showTab=8&view=list')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/raw_materials?showTab=8&view=list')

# Raw Material Process


@app.route("/raw_materials/process/update/<id>", methods=['POST'])
@login_required
def process_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    process_form = FabProcForm()
    if process_form.proc_update.data:
        process_name = str(process_form.proc.data).lower()
        check_one = db.session.query(
            FabProc).filter_by(id=id).first()
        if check_one is not None:
            check_one.process = process_name
            check_one.desc = process_form.desc.data
            db.session.commit()
            session['mssg'] = "Process updated successfully"
            return redirect('/raw_materials?showTab=9&view=list')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/raw_materials?showTab=9&view=list')


@app.route("/raw_materials/process/delete/<id>", methods=['POST', 'GET'])
@login_required
def process_delete(id):

    check_one = db.session.query(
        FabProc).filter_by(id=id)
    if check_one.first() is not None:
        if len(check_one.first().proc_goods) is int(0):
            check_one.delete()
            db.session.commit()
            session['mssg'] = "Process deleted successfully"
            return redirect('/raw_materials?showTab=9&view=list')
        else:
            session['mssg'] = "Cannot delete. Value is being used."
            return redirect('/raw_materials?showTab=9&view=list')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/raw_materials?showTab=9&view=list')


# Raw Material Category  Edits

@app.route("/raw_materials/cat/update/<id>", methods=['POST'])
@login_required
def cat_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    cat_form = RawCatForm()
    if cat_form.cat_update.data:
        cat_name = str(cat_form.cat.data).lower()
        check_one = db.session.query(
            RawCat).filter_by(id=id).first()
        if check_one is not None:
            check_one.cat = cat_name
            check_one.desc = cat_form.desc.data
            db.session.commit()
            session['mssg'] = "Category updated successfully"
            return redirect('/raw_materials?showTab=12&view=list')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/raw_materials?showTab=12&view=list')


@app.route("/raw_materials/cat/delete/<id>", methods=['POST', 'GET'])
@login_required
def cat_delete(id):

    check_one = db.session.query(
        RawCat).filter_by(id=id)
    if check_one.first() is not None:
        if len(check_one.first().cat_fab_goods) is int(0):
            check_one.delete()
            db.session.commit()
            session['mssg'] = "Category deleted successfully"
            return redirect('/raw_materials?showTab=12&view=list')
        else:
            session['mssg'] = "Cannot delete. Value is being used."
            return redirect('/raw_materials?showTab=12&view=list')
        
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/raw_materials?showTab=12&view=list')


# Raw Material Width  Edits

@app.route("/raw_materials/width/update/<id>", methods=['POST'])
@login_required
def width_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    width_form = FabWidthForm()
    if width_form.width_update.data:
        width_name = str(width_form.width.data).lower()
        check_one = db.session.query(
            FabWidth).filter_by(id=id).first()
        if check_one is not None:
            check_one.width = width_name
            db.session.commit()
            session['mssg'] = "Width updated successfully"
            return redirect('/raw_materials?showTab=10&view=list')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/raw_materials?showTab=10&view=list')


@app.route("/raw_materials/width/delete/<id>", methods=['POST', 'GET'])
@login_required
def width_delete(id):

    check_one = db.session.query(
        FabWidth).filter_by(id=id)
    if check_one.first() is not None:
        if len(check_one.first().width_goods) is 0:
            check_one.delete()
            db.session.commit()
            session['mssg'] = "Width deleted successfully"
            return redirect('/raw_materials?showTab=10&view=list')
        else:
            session['mssg'] = "Cannot delete. Value is being used."
            return redirect('/raw_materials?showTab=10&view=list')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/raw_materials?showTab=10&view=list')


# Raw Material Dye  Edits

@app.route("/raw_materials/dye/update/<id>", methods=['POST'])
@login_required
def dye_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    dye_form = FabDyeForm()
    if dye_form.dye_update.data:
        dye_name = str(dye_form.dye.data).lower()
        check_one = db.session.query(
            FabDye).filter_by(id=id).first()
        if check_one is not None:
            check_one.dye = dye_name
            db.session.commit()
            session['mssg'] = "Dye updated successfully"
            return redirect('/raw_materials?showTab=11&view=list')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/raw_materials?showTab=11&view=list')


@app.route("/raw_materials/dye/delete/<id>", methods=['POST', 'GET'])
@login_required
def dye_delete(id):

    check_one = db.session.query(
        FabDye).filter_by(id=id)
    if check_one.first() is not None:
        if len(check_one.first().dye_goods) is int(0):
            check_one.delete()
            db.session.commit()
            session['mssg'] = "Dye deleted successfully"
            return redirect('/raw_materials?showTab=11&view=list')
        else:
            session['mssg'] = "Cannot delete. Value is being used."
            return redirect('/raw_materials?showTab=11&view=list')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/raw_materials?showTab=11&view=list')

# Raw Material Construction  Edits


@app.route("/raw_materials/const/update/<id>", methods=['POST'])
@login_required
def const_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    const_form = FabConstForm()
    if const_form.const_update.data:
        const_name = str(const_form.const.data).lower()
        check_one = db.session.query(
            FabConst).filter_by(id=id).first()
        if check_one is not None:
            check_one.const = const_name
            db.session.commit()
            session['mssg'] = "Construction updated successfully"
            return redirect('/raw_materials?showTab=13&view=list')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/raw_materials?showTab=13&view=list')


@app.route("/raw_materials/const/delete/<id>", methods=['POST', 'GET'])
@login_required
def const_delete(id):

    check_one = db.session.query(
        FabConst).filter_by(id=id)
    if check_one.first() is not None:
        if len(check_one.first().const_goods) is int(0):
            check_one.delete()
            db.session.commit()
            session['mssg'] = "Construction deleted successfully"
            return redirect('/raw_materials?showTab=13&view=list')
        else:
            session['mssg'] = "Cannot delete. Value is being used."
            return redirect('/raw_materials?showTab=13&view=list')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/raw_materials?showTab=13&view=list')

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
    session['dup'] = ""

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

@app.route('/fin_goods/delete/<id>', methods=["POST", "GET"])
@login_required
def fin_goods_delete(id):
    try:
        data_get = db.session.query(FinGoods).filter_by(id=int(id)).first().get_gen_name()
        db.session.query(FinGoods).filter_by(id=int(id)).delete()
        db.session.commit()
        session["mssg"] = "Finished Goods - "+str(data_get)+" is deleted."
        return redirect('/main_master?showTab=14&view=list')
    except Exception as e:
        logging.error('Error deleting Finished Goods : ' + str(e))
        session["mssg"] = "Couldn't delete firm."
        return redirect('/main_master?showTab=14&view=list')


@app.route('/fin_goods/update/<id>', methods=["POST"])
@login_required
def fin_goods_update(id):
    if request.method == "POST":
        payload = request.json
        fin_good = db.session.query(Trans).filter_by(id = int(id)).first()
        new_fin_good.product_category.clear()
        fin_good.product_category.append()
        db.session.commit()
        session['mssg'] = "Transaction - Part B with PP No. " + str( pp_num.id) + " has been added."
        return jsonify("success")
    
@app.route('/raw_goods/delete/<id>', methods=["POST", "GET"])
@login_required
def raw_goods_delete(id):
    try:
        data_get = db.session.query(RawFabMain).filter_by(id=int(id)).first().get_gen_name()
        db.session.query(RawFabMain).filter_by(id=int(id)).delete()
        db.session.commit()
        session["mssg"] = "Raw Fabric Material - "+str(data_get)+" is deleted."
        return redirect('/main_master?showTab=15&view=list')
    except Exception as e:
        logging.error('Error deleting Finished Goods : ' + str(e))
        session["mssg"] = "Couldn't delete Raw Fabric Material."
        return redirect('/main_master?showTab=15&view=list')



########################################################
########## APIs for Transaction Masters ################
########################################################

@app.route('/semi_save_trans' , methods = ['POST'])
@login_required
def save_trans():
    payload = request.json

    pp_num = Trans()
    pp_num.flag = 3
    pp_num.part_a = json.dumps(payload)
    pp_num.part_b = "{}"
    db.session.add(pp_num)
    db.session.commit()
    session['mssg'] = "Transaction - "+str(payload['PP_no'])+" saved as draft."
    return jsonify("success")

@app.route('/get/raw_product/' , methods=["GET"])
@login_required 
def get_raw_prod():
    res = db.session.query(RawFabMain).all()
    data = []
    for r in res:
        p_id = str(r.id)
        p_name = str(r.get_gen_name())
        temp_tup = (p_id , p_name)
        data.append(temp_tup)

    obj = '{' + ', '.join('"{}": "{}"'.format(k, v) for k, v in data) + '}'
    return obj

@app.route('/get/fin_product/' , methods=["GET"])
@login_required 
def get_fin_prod():
    res = db.session.query(FinGoods).all()
    data = []
    for r in res:
        p_id = str(r.id)
        p_name = str(r.get_gen_name())
        temp_tup = (p_id , p_name)
        data.append(temp_tup)
    obj = '{' + ', '.join('"{}": "{}"'.format(k, v) for k, v in data) + '}'
    return obj

@app.route('/get/fin_product/<fin_id>' , methods=["GET"])
@login_required 
def get_fin_prod_by_id(fin_id):
    res = db.session.query(FinGoods).filter_by(id = int(fin_id)).first()

    p_name = str(res.get_gen_name())
    return jsonify(p_name)
    
@app.route('/get/uom/' , methods=["GET"])
@login_required 
def get_uom():
    res = db.session.query(Uom).all()
    data = []
    for r in res:
        p_id = str(r.id)
        p_name = str(r.measure)
        temp_tup = (p_id , p_name)
        data.append(temp_tup)
    obj = '{' + ', '.join('"{}": "{}"'.format(k, v) for k, v in data) + '}'
    return obj
    
@app.route('/get/uom/<fin_id>' , methods=["GET"])
@login_required 
def get_uom_by_id(fin_id):
    res = db.session.query(FinGoods).filter_by(id = int(fin_id)).first().uom[0].measure
    return jsonify(res)
    
@app.route('/get/uom/raw_fab/<fin_id>' , methods=["GET"])
@login_required 
def get_uom_by_id_raw_fab(fin_id):
    res = db.session.query(RawFabMain).filter_by(id = int(fin_id)).first().uom[0].measure
    return jsonify(res)
    

@app.route('/get/uom/acc/<fin_id>' , methods=["GET"])
@login_required 
def get_uom_by_id_acc(fin_id):
    res = db.session.query(Accessories).filter_by(id = int(fin_id)).first().uom[0].measure
    return jsonify(res)

@app.route('/get/uom/oth/<fin_id>' , methods=["GET"])
@login_required 
def get_uom_by_id_oth(fin_id):
    res = db.session.query(OtherMat).filter_by(id = int(fin_id)).first().uom[0].measure
    return jsonify(res)

@app.route('/get/acc/' , methods=["GET"])
@login_required 
def get_acc():
    res = db.session.query(Accessories).all()
    data = []
    for r in res:
        p_id = str(r.id)
        p_name = str(r.acc)
        temp_tup = (p_id , p_name)
        data.append(temp_tup)
    obj = '{' + ', '.join('"{}": "{}"'.format(k, v) for k, v in data) + '}'
    return obj

@app.route('/get/oth_mat/' , methods=["GET"])
@login_required 
def get_oth_mat():
    res = db.session.query(OtherMat).all()
    data = []
    for r in res:
        p_id = str(r.id)
        p_name = str(r.mat)
        temp_tup = (p_id , p_name)
        data.append(temp_tup)
    obj = '{' + ', '.join('"{}": "{}"'.format(k, v) for k, v in data) + '}'
    return obj

@app.route('/get/trans_pp/' , methods=["GET"])
@login_required 
def get_trans_pp():
    res =   db.session.query(Trans).filter_by(flag=0).all()
    data = []
    for r in res:
        p_id = str(r.id)
        temp_tup = (str(p_id) , str(p_id))
        data.append(temp_tup)
    obj = '{' + ', '.join('"{}": "{}"'.format(k, v) for k, v in data) + '}'
    return obj


@app.route('/get/trans_pp_b' , methods=["GET"])
@login_required 
def get_detail_pp():
    pp_num = request.args.get('pp_num')
    res = db.session.query(Trans).filter_by(id = str(pp_num)).first()

    payload = json.loads(res.part_b)
    return jsonify(payload)


@app.route('/get/trans_pp/meta' , methods=["GET"])
@login_required 
def get_meta_pp():
    pp_num = request.args.get('pp_num')
    res = db.session.query(Trans).filter_by(id = str(pp_num)).first()

    payload = json.loads(res.meta)
    return jsonify(payload)


@app.route('/get/trans_pp_a/<trans_id>' , methods=["GET"])
@login_required 
def get_detail_pp_a(trans_id):
    
    res = db.session.query(Trans).filter_by(id = int(trans_id)).first()

    payload = json.loads(res.part_a)
    return jsonify(payload)
   
@app.route('/get/unit/locations' , methods=["GET"])
@login_required
def get_location():
    res  = db.session.query(UnitLoc).all()
    data = []
    for r in res:
        p_id = str(r.id)
        p_name = str(r.unit)
        temp_tup = (p_id , p_name)
        data.append(temp_tup)
    obj = '{' + ', '.join('"{}": "{}"'.format(k, v) for k, v in data) + '}'
    return obj

@app.route('/close_trans' , methods = ['POST'])
@login_required
def close_trans():
    payload = request.json
    pp_num = db.session.query(Trans).filter_by(id = str(payload['pp_num'])).first()
    pp_num.flag = 1
    db.session.commit()
    session['mssg'] = "Transaction - "+str(payload['pp_num'])+" has been closed."
    return jsonify("success")

@app.route('/delete_trans/<trans_id>' , methods = ['POST'])
@login_required
def delete_trans(trans_id):
    trans = db.session.query(Trans).filter_by(id = int(trans_id)).first()
    trans.flag = 2 # flag for soft delete
    db.session.commit()
    return jsonify("success")

@app.route('/save/dept/cut' , methods = ['GET' , 'POST'])
@login_required
def add_dept_cut():
    payload = request.json
    try:
        for k,v in payload["pp_sel"].items():
            pp_num = db.session.query(Trans).filter_by(id = int(v)).first()
            part_b = json.loads(pp_num.part_b)
            key_len = len(part_b["cut_datefilter"])
            part_b["cut_datefilter"][str(key_len)] = payload["cut_datefilter"][str(k)]
            part_b["cut_qty"][str(key_len)] = payload["cut_qty"][str(k)]
            part_b["cut_loc"][str(key_len)] = payload["unit_loc"][str(k)]
            part_b["cut_rem"][str(key_len)] = payload["cut_rem"][str(k)]
            pp_num.part_b = json.dumps(part_b)
            db.session.commit()
        session['mssg'] = "Data successfully added."
        return jsonify("success")
    except Exception as e:
        session['mssg'] = "Somethign unexpected happened - "+str(e)
        return jsonify("success")

@app.route('/save/dept/stitch' , methods = ['GET' , 'POST'])
@login_required
def add_dept_sth():
    payload = request.json
    try:
        for k,v in payload["pp_sel"].items():
            pp_num = db.session.query(Trans).filter_by(id = int(v)).first()
            part_b = json.loads(pp_num.part_b)
            key_len = len(part_b["sth_datefilter"])
            part_b["sth_datefilter"][str(key_len)] = payload["sth_datefilter"][str(k)]
            part_b["sth_qty"][str(key_len)] = payload["sth_qty"][str(k)]
            part_b["sth_loc"][str(key_len)] = payload["unit_loc"][str(k)]
            part_b["sth_rem"][str(key_len)] = payload["sth_rem"][str(k)]
            pp_num.part_b = json.dumps(part_b)
            db.session.commit()
        session['mssg'] = "Data successfully added."
        return jsonify("success")
    except Exception as e:
        session['mssg'] = "Somethign unexpected happened - "+str(e)
        return jsonify("success")


@app.route('/save/dept/val' , methods = ['GET' , 'POST'])
@login_required
def add_dept_val():
    payload = request.json
    try:
        for k,v in payload["pp_sel"].items():
            pp_num = db.session.query(Trans).filter_by(id = int(v)).first()
            part_b = json.loads(pp_num.part_b)
            key_len = len(part_b["val_datefilter"])
            part_b["val_datefilter"][str(key_len)] = payload["val_datefilter"][str(k)]
            part_b["val_qty"][str(key_len)] = payload["val_qty"][str(k)]
            part_b["val_loc"][str(key_len)] = payload["unit_loc"][str(k)]
            part_b["val_rem"][str(key_len)] = payload["val_rem"][str(k)]
            pp_num.part_b = json.dumps(part_b)
            db.session.commit()
        session['mssg'] = "Data successfully added."
        return jsonify("success")
    except Exception as e:
        session['mssg'] = "Somethign unexpected happened - "+str(e)
        return jsonify("success")

@app.route('/save/dept/kaj' , methods = ['GET' , 'POST'])
@login_required
def add_dept_kaj():
    payload = request.json
    try:
        for k,v in payload["pp_sel"].items():
            pp_num = db.session.query(Trans).filter_by(id = int(v)).first()
            part_b = json.loads(pp_num.part_b)
            key_len = len(part_b["kaj_datefilter"])
            part_b["kaj_datefilter"][str(key_len)] = payload["kaj_datefilter"][str(k)]
            part_b["kaj_qty"][str(key_len)] = payload["kaj_qty"][str(k)]
            part_b["kaj_loc"][str(key_len)] = payload["unit_loc"][str(k)]
            part_b["kaj_rem"][str(key_len)] = payload["kaj_rem"][str(k)]
            pp_num.part_b = json.dumps(part_b)
            db.session.commit()
        session['mssg'] = "Data successfully added."
        return jsonify("success")
    except Exception as e:
        logging.error(str(e))
        session['mssg'] = "Somethign unexpected happened - "+str(e)
        return jsonify("success")

@app.route('/save/dept/tes' , methods = ['GET' , 'POST'])
@login_required
def add_dept_tes():
    payload = request.json
    try:
        for k,v in payload["pp_sel"].items():
            pp_num = db.session.query(Trans).filter_by(id = int(v)).first()
            part_b = json.loads(pp_num.part_b)
            key_len = len(part_b["tes_datefilter"])
            part_b["tes_datefilter"][str(key_len)] = payload["tes_datefilter"][str(k)]
            part_b["tes_qty"][str(key_len)] = payload["tes_qty"][str(k)]
            part_b["tes_loc"][str(key_len)] = payload["unit_loc"][str(k)]
            part_b["tes_rem"][str(key_len)] = payload["tes_rem"][str(k)]
            pp_num.part_b = json.dumps(part_b)
            db.session.commit()
        session['mssg'] = "Data successfully added."
        return jsonify("success")
    except Exception as e:
        logging.error(str(e))
        session['mssg'] = "Somethign unexpected happened - "+str(e)
        return jsonify("success")

@app.route('/save/dept/thr' , methods = ['GET' , 'POST'])
@login_required
def add_dept_thr():
    payload = request.json
    try:
        for k,v in payload["pp_sel"].items():
            pp_num = db.session.query(Trans).filter_by(id = int(v)).first()
            part_b = json.loads(pp_num.part_b)
            key_len = len(part_b["thr_datefilter"])
            part_b["thr_datefilter"][str(key_len)] = payload["thr_datefilter"][str(k)]
            part_b["thr_qty"][str(key_len)] = payload["thr_qty"][str(k)]
            part_b["thr_loc"][str(key_len)] = payload["unit_loc"][str(k)]
            part_b["thr_rem"][str(key_len)] = payload["thr_rem"][str(k)]
            pp_num.part_b = json.dumps(part_b)
            db.session.commit()
        session['mssg'] = "Data successfully added."
        return jsonify("success")
    except Exception as e:
        logging.error(str(e))
        session['mssg'] = "Somethign unexpected happened - "+str(e)
        return jsonify("success")

@app.route('/save/dept/qc' , methods = ['GET' , 'POST'])
@login_required
def add_dept_qc():
    payload = request.json
    try:
        for k,v in payload["pp_sel"].items():
            pp_num = db.session.query(Trans).filter_by(id = int(v)).first()
            part_b = json.loads(pp_num.part_b)
            key_len = len(part_b["qc_datefilter"])
            part_b["qc_datefilter"][str(key_len)] = payload["qc_datefilter"][str(k)]
            part_b["qc_qty"][str(key_len)] = payload["qc_qty"][str(k)]
            part_b["qc_loc"][str(key_len)] = payload["unit_loc"][str(k)]
            part_b["qc_rem"][str(key_len)] = payload["qc_rem"][str(k)]
            pp_num.part_b = json.dumps(part_b)
            db.session.commit()
        session['mssg'] = "Data successfully added."
        return jsonify("success")
    except Exception as e:
        logging.error(str(e))
        session['mssg'] = "Somethign unexpected happened - "+str(e)
        return jsonify("success")

@app.route('/save/dept/pre' , methods = ['GET' , 'POST'])
@login_required
def add_dept_pre():
    payload = request.json
    try:
        for k,v in payload["pp_sel"].items():
            pp_num = db.session.query(Trans).filter_by(id = int(v)).first()
            part_b = json.loads(pp_num.part_b)
            key_len = len(part_b["pre_datefilter"])
            part_b["pre_datefilter"][str(key_len)] = payload["pre_datefilter"][str(k)]
            part_b["pre_qty"][str(key_len)] = payload["pre_qty"][str(k)]
            part_b["pre_loc"][str(key_len)] = payload["unit_loc"][str(k)]
            part_b["pre_rem"][str(key_len)] = payload["pre_rem"][str(k)]
            pp_num.part_b = json.dumps(part_b)
            db.session.commit()
        session['mssg'] = "Data successfully added."
        return jsonify("success")
    except Exception as e:
        logging.error(str(e))
        session['mssg'] = "Somethign unexpected happened - "+str(e)
        return jsonify("success")

@app.route('/save/dept/tag' , methods = ['GET' , 'POST'])
@login_required
def add_dept_tag():
    payload = request.json
    try:
        for k,v in payload["pp_sel"].items():
            pp_num = db.session.query(Trans).filter_by(id = int(v)).first()
            part_b = json.loads(pp_num.part_b)
            key_len = len(part_b["tag_datefilter"])
            part_b["tag_datefilter"][str(key_len)] = payload["tag_datefilter"][str(k)]
            part_b["tag_qty"][str(key_len)] = payload["tag_qty"][str(k)]
            part_b["tag_loc"][str(key_len)] = payload["unit_loc"][str(k)]
            part_b["tag_rem"][str(key_len)] = payload["tag_rem"][str(k)]
            pp_num.part_b = json.dumps(part_b)
            db.session.commit()
        session['mssg'] = "Data successfully added."
        return jsonify("success")
    except Exception as e:
        logging.error(str(e))
        session['mssg'] = "Somethign unexpected happened - "+str(e)
        return jsonify("success")

@app.route('/save/dept/tra' , methods = ['GET' , 'POST'])
@login_required
def add_dept_tra():
    payload = request.json
    try:
        for k,v in payload["pp_sel"].items():
            pp_num = db.session.query(Trans).filter_by(id = int(v)).first()
            part_b = json.loads(pp_num.part_b)
            key_len = len(part_b["tra_datefilter"])
            part_b["tra_datefilter"][str(key_len)] = payload["tra_datefilter"][str(k)]
            part_b["tra_qty"][str(key_len)] = payload["tra_qty"][str(k)]
            part_b["tra_loc"][str(key_len)] = payload["unit_loc"][str(k)]
            part_b["tra_rem"][str(key_len)] = payload["tra_rem"][str(k)]
            pp_num.part_b = json.dumps(part_b)
            db.session.commit()
        session['mssg'] = "Data successfully added."
        return jsonify("success")
    except Exception as e:
        logging.error(str(e))
        session['mssg'] = "Somethign unexpected happened - "+str(e)
        return jsonify("success")