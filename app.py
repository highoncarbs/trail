

from flask import Flask, render_template, g, redirect, jsonify, url_for, request, session
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)


migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from model import Users, LoginForm, SignupForm, CustomerCategory, CustomerCategoryForm, City, State, Country,\
    CityForm, StateForm, CountryForm, Firms, FirmForm, Uom, UomForm, Yarn, YarnForm, FabConst, FabConstForm, \
    FabProc, FabProcForm,  FabWidth, FabWidthForm, FabDye, FabDyeForm, RawCat, RawCatForm , FinCat , FinCatForm ,\
    FabComb , FabCombForm , PrintTech , PrintTechForm , FinDes , FinDesForm , FinSize , FinSizeForm
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
    if not hasattr(session, "mssg"):
        session['mssg'] = ""
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


@app.route('/user-roles', methods=['GET', 'POST'])
@login_required
def user_roles():
    form = SignupForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None:
            hashed_pass = generate_password_hash(
                form.password.data, method='sha256')
            new_user = Users(username=form.username.data,
                             password=hashed_pass)
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

    return render_template('user_roles.html', subtitle="User Roles", mssg=session['mssg'], form=form), 200

# Basic Master Views
#
#

# Customer Category MAster


@app.route('/basic_master/customer_category', methods=['GET', 'POST'])
@login_required
def customer_category():
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
                return redirect(url_for('customer_category'))
    return render_template('customer_Category.html', subtitle="Customer Category", mssg=session['mssg'], cust_form=cust_form), 200


@app.route('/basic_master/customer_category_view', methods=['GET', 'POST'])
@login_required
def customer_category_view():
    cust_list = db.session.query(
        CustomerCategory).all()
    cust_form = CustomerCategoryForm()

    return render_template('customer_category_view.html', subtitle="Customer Category", mssg=session['mssg'], cust_list=cust_list, cust_form=cust_form), 200

# UOM Master


@app.route('/basic_master/uom', methods=['GET', 'POST'])
@login_required
def uom():
    uom_list = db.session.query(
        Uom).all()
    uom_form = UomForm()

    if uom_form.validate_on_submit():
        if uom_form.uom_submit.data:
            uom_name = str(uom_form.measure.data)
            check_one = db.session.query(
                Uom).filter_by(measure=uom_name).first()
            if check_one is None:
                new_uom = Uom(measure=uom_name, desc=uom_form.desc.data,
                              decimal=int(uom_form.decimal.data))
                db.session.add(new_uom)
                db.session.commit()
                return redirect(url_for('uom'))
    return render_template('uom_master.html', subtitle="Unit of Measurement", mssg=session['mssg'], uom_form=uom_form), 200


# Location Master


@app.route('/basic_master/location', methods=['GET', 'POST'])
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
                mssg = "City already exists "
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
            if check_one is None:
                new_country = Country(country=country_name)
                db.session.add(new_country)
                db.session.commit()
                return redirect('/location')    
    
    return render_template('location_master.html', subtitle="Location", mssg=session['mssg'], city_form=city_form, city_list=city_list,
                           state_form=state_form, state_list=state_list, country_form=country_form, country_list=country_list), 200

@app.route('/basic_master/uom_view', methods=['GET', 'POST'])
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
            cat_name = str(cat_form.cat.data)
            check_one = db.session.query(
                FinCat).filter_by(cat=cat_name).first()
            if check_one is not None:
                session['mssg'] = "Fabric Process already exists "
            else:
                new_cat = FinCat(
                    cat=cat_name, desc=cat_form.desc.data)
                db.session.add(new_cat)
                db.session.commit()
                session['mssg'] = "Fabric Process - " + \
                    cat_name+"  successfully added."
                return redirect('/finished_goods')

    comb_list = db.session.query(
        FabComb).all()
    comb_form = FabCombForm()

    if comb_form.validate_on_submit():
        if comb_form.comb_submit.data:
            comb_name = str(comb_form.comb.data)
            check_one = db.session.query(
                FabComb).filter_by(comb=comb_name).first()
            if check_one is not None:
                session['mssg'] = "Fabric Process already exists "
            else:
                new_comb = FabComb(
                    comb=comb_name, desc=comb_form.desc.data)
                db.session.add(new_comb)
                db.session.commit()
                session['mssg'] = "Fabric Process - " + \
                    comb_name+"  successfully added."
                return redirect('/finished_goods')
    
    tech_list = db.session.query(
        PrintTech).all()
    tech_form = PrintTechForm()

    if tech_form.validate_on_submit():
        if tech_form.tech_submit.data:
            tech_name = str(tech_form.tech.data)
            check_one = db.session.query(
                PrintTech).filter_by(tech=tech_name).first()
            if check_one is not None:
                session['mssg'] = "Fabric Process already exists "
            else:
                new_tech = PrintTech(
                    tech=tech_name, desc=tech_form.desc.data)
                db.session.add(new_tech)
                db.session.commit()
                session['mssg'] = "Fabric Process - " + \
                    tech_name+"  successfully added."
                return redirect('/finished_goods')

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
            else:
                new_des = FinDes(des=des_name)
                db.session.add(new_des)
                db.session.commit()
                session['mssg'] = "Design - " + \
                    des_name+" successfully added."
                return redirect('/finished_goods')
    
    size_list = db.session.query(
        FinSize).all()
    size_form = FinSizeForm()

    if size_form.validate_on_submit():
        if size_form.size_submit.data:
            size_name = str(size_form.size.data)
            check_one = db.session.query(
                FinSize).filter_by(size=size_name).first()
            if check_one is not None:
                session['mssg'] = "Size already exists "
            else:
                new_size = FinSize(size=size_name)
                db.session.add(new_size)
                db.session.commit()
                session['mssg'] = "Size - " + \
                    size_name+" successfully added."
                return redirect('/finished_goods')

    return render_template('fin_goods.html' , subtitle = "Finished Goods " , mssg = session['mssg'] , cat_list =cat_list ,cat_form = cat_form ,\
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
        cat_name = str(cat_form.cat.data).title()
        check_one = db.session.query(
            FinCat).filter_by(id=id).first()
        if check_one is not None:
            check_one.cat = cat_name
            check_one.desc = cat_form.desc.data
            db.session.commit()
            session['mssg'] = "Finished Goods Category updated successfully"
            return redirect('/finished_goods')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/finished_goods')


@app.route("/finished_goods/cat/delete/<id>", methods=['POST', 'GET'])
@login_required
def pcat_delete(id):

    check_one = db.session.query(
        FinCat).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "Category deleted successfully"
        return redirect('/finished_goods')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/finished_goods')

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
        comb_name = str(comb_form.comb.data).title()
        check_one = db.session.query(
            FabComb).filter_by(id=id).first()
        if check_one is not None:
            check_one.comb = comb_name
            check_one.desc = comb_form.desc.data
            db.session.commit()
            session['mssg'] = "Finished Goods Category updated successfully"
            return redirect('/finished_goods')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/finished_goods')


@app.route("/finished_goods/comb/delete/<id>", methods=['POST', 'GET'])
@login_required
def comb_delete(id):

    check_one = db.session.query(
        FabComb).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "Category deleted successfully"
        return redirect('/finished_goods')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/finished_goods')

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
        tech_name = str(tech_form.tech.data).title()
        check_one = db.session.query(
            PrintTech).filter_by(id=id).first()
        if check_one is not None:
            check_one.tech = tech_name
            check_one.desc = tech_form.desc.data
            db.session.commit()
            session['mssg'] = "Print Technique updated successfully"
            return redirect('/finished_goods')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/finished_goods')


@app.route("/finished_goods/tech/delete/<id>", methods=['POST', 'GET'])
@login_required
def tech_delete(id):

    check_one = db.session.query(
        PrintTech).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "Print Technique deleted successfully"
        return redirect('/finished_goods')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/finished_goods')


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
        des_name = str(des_form.des.data).title()
        check_one = db.session.query(
            FinDes).filter_by(id=id).first()
        if check_one is not None:
            check_one.des = des_name
            db.session.commit()
            session['mssg'] = "Fabric Design updated successfully"
            return redirect('/finished_goods')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/finished_goods')


@app.route("/finished_goods/des/delete/<id>", methods=['POST', 'GET'])
@login_required
def des_delete(id):

    check_one = db.session.query(
        FinDes).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "Fabric Design deleted successfully"
        return redirect('/finished_goods')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/finished_goods')

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
        size_name = str(size_form.size.data).title()
        check_one = db.session.query(
            FinSize).filter_by(id=id).first()
        if check_one is not None:
            check_one.size = size_name
            db.session.commit()
            session['mssg'] = "Fabric Size updated successfully"
            return redirect('/finished_goods')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/finished_goods')


@app.route("/finished_goods/size/delete/<id>", methods=['POST', 'GET'])
@login_required
def size_delete(id):

    check_one = db.session.query(
        FinSize).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "Fabric Size deleted successfully"
        return redirect('/finished_goods')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/finished_goods')


@app.route('/other_materials', methods=['GET', 'POST'])
@login_required
def other_materials():
    pass
@app.route('/firms', methods=['GET', 'POST'])
@login_required
def firms():
    pass

@app.route('/basic_master', methods=['GET', 'POST'])
@login_required
def basic_master():
    pass


from model import FinGoodsForm , RawFabMainForm
@app.route('/main_master', methods=['GET', 'POST'])
@login_required
def main_master():
    fin_goods_form = FinGoodsForm()
    raw_form = RawFabMainForm()
    return render_template('main_master.html' , fin_form = fin_goods_form , raw_form = raw_form) ,200


@app.route('/raw_materials', methods=['GET', 'POST'])
@login_required
def raw_materials():
 

    # Yarn Form

    yarn_list = db.session.query(
        Yarn).all()
    yarn_form = YarnForm()

    if yarn_form.validate_on_submit():
        if yarn_form.yarn_submit.data:
            yarn_name = str(yarn_form.yarn.data)
            check_one = db.session.query(
                Yarn).filter_by(yarn=yarn_name).first()
            if check_one is not None:
                session['mssg'] = "Yarn already exists "
            else:
                new_yarn = Yarn(yarn=yarn_name, desc=yarn_form.desc.data)
                db.session.add(new_yarn)
                db.session.commit()
                session['mssg'] = "Yarn - "+yarn_name+" successfully added."
                return redirect('/raw_materials')

    # Fabric Construction Form

    const_list = db.session.query(
        FabConst).all()
    const_form = FabConstForm()

    if const_form.validate_on_submit():
        if const_form.const_submit.data:
            const_name = str(const_form.const.data)
            check_one = db.session.query(
                FabConst).filter_by(const=const_name).first()
            if check_one is not None:
                session['mssg'] = "Construction already exists "
            else:
                new_const = FabConst(const=const_name)
                db.session.add(new_const)
                db.session.commit()
                session['mssg'] = "Construction - " + \
                    const_name+" successfully added."
                return redirect('/raw_materials')

    # Fabric process Form

    process_list = db.session.query(
        FabProc).all()
    process_form = FabProcForm()

    if process_form.validate_on_submit():
        if process_form.proc_submit.data:
            process_name = str(process_form.proc.data)
            check_one = db.session.query(
                FabProc).filter_by(process=process_name).first()
            if check_one is not None:
                session['mssg'] = "Fabric Process already exists "
            else:
                new_process = FabProc(
                    process=process_name, desc=process_form.desc.data)
                db.session.add(new_process)
                db.session.commit()
                session['mssg'] = "Fabric Process - " + \
                    process_name+"  successfully added."
                return redirect('/raw_materials')

    # Fabric Width Form

    width_list = db.session.query(
        FabWidth).all()
    width_form = FabWidthForm()

    if width_form.validate_on_submit():
        if width_form.width_submit.data:
            width_name = str(width_form.width.data)
            check_one = db.session.query(
                FabWidth).filter_by(width=width_name).first()
            if check_one is not None:
                session['mssg'] = "Fabric Width already exists "
            else:
                new_width = FabWidth(width=width_name)
                db.session.add(new_width)
                db.session.commit()
                session['mssg'] = "Fabric Width - " + \
                    width_name+"  successfully added."
                return redirect('/raw_materials')

    # Fabric Dye Form

    dye_list = db.session.query(
        FabDye).all()
    dye_form = FabDyeForm()

    if dye_form.validate_on_submit():
        if dye_form.dye_submit.data:
            dye_name = str(dye_form.dye.data)
            check_one = db.session.query(
                FabDye).filter_by(dye=dye_name).first()
            if check_one is not None:
                session['mssg'] = "Fabric Dye already exists "
            else:
                new_dye = FabDye(dye=dye_name)
                db.session.add(new_dye)
                db.session.commit()
                session['mssg'] = "Fabric Dye - " + \
                    dye_name+"  successfully added."
                return redirect('/raw_materials')

    # Raw Mat Cateogry Form

    cat_list = db.session.query(
        RawCat).all()
    cat_form = RawCatForm()

    if cat_form.validate_on_submit():
        if cat_form.cat_submit.data:
            cat_name = str(cat_form.cat.data)
            check_one = db.session.query(
                RawCat).filter_by(cat=cat_name).first()
            if check_one is not None:
                session['mssg'] = "Raw Material Category already exists "
            else:
                new_cat = RawCat(cat=cat_name, desc=cat_form.desc.data)
                db.session.add(new_cat)
                db.session.commit()
                session['mssg'] = "Category - " + \
                    cat_name+"  successfully added."
                return redirect('/raw_materials')

    return render_template('raw_mat_master.html', subtitle="Basic Master", mssg=session['mssg'],
                           yarn_list=yarn_list,  yarn_form=yarn_form,  const_list=const_list, const_form=const_form,
                           width_list=width_list, width_form=width_form,  process_list=process_list, process_form=process_form,
                           dye_list=dye_list, dye_form=dye_form, cat_list=cat_list, cat_form=cat_form), 200




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
            return redirect('/raw_materials')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/raw_materials')


@app.route("/basic_master/state/delete/<id>", methods=['POST', 'GET'])
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
            return redirect('/raw_materials')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/raw_materials')


@app.route("/basic_master/country/delete/<id>", methods=['POST', 'GET'])
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
            return redirect('/raw_materials')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/raw_materials')


@app.route("/basic_master/city/delete/<id>", methods=['POST', 'GET'])
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
            return redirect('/raw_materials')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/raw_materials')


@app.route("/basic_master/health/delete/<id>", methods=['POST', 'GET'])
@login_required
def cust_delete(id):

    check_one = db.session.query(
        CustomerCategory).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "Customer Category deleted successfully"
        return redirect('/raw_materials')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/raw_materials')


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
            return redirect('/raw_materials')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/raw_materials')


@app.route("/basic_master/uom/delete/<id>", methods=['POST', 'GET'])
@login_required
def uom_delete(id):

    check_one = db.session.query(
        Uom).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "Measure deleted successfully"
        return redirect('/raw_materials')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/raw_materials')


# Raw MAterial Yarn  Edits

@app.route("/basic_master/yarn/update/<id>", methods=['POST'])
@login_required
def yarn_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    yarn_form = YarnForm()
    if yarn_form.yarn_update.data:
        yarn_name = str(yarn_form.yarn.data)
        check_one = db.session.query(
            Yarn).filter_by(id=id).first()
        if check_one is not None:
            check_one.yarn = yarn_name
            check_one.desc = yarn_form.desc.data
            db.session.commit()
            session['mssg'] = "Yarn updated successfully"
            return redirect('/raw_materials')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/raw_materials')


@app.route("/basic_master/yarn/delete/<id>", methods=['POST', 'GET'])
@login_required
def yarn_delete(id):

    check_one = db.session.query(
        Yarn).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "Yarn deleted successfully"
        return redirect('/raw_materials')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/raw_materials')

# Raw MAterial Process


@app.route("/basic_master/process/update/<id>", methods=['POST'])
@login_required
def process_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    process_form = FabProcForm()
    if process_form.proc_update.data:
        process_name = str(process_form.proc.data)
        check_one = db.session.query(
            FabProc).filter_by(id=id).first()
        if check_one is not None:
            check_one.process = process_name
            check_one.desc = process_form.desc.data
            db.session.commit()
            session['mssg'] = "Process updated successfully"
            return redirect('/raw_materials')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/raw_materials')


@app.route("/basic_master/process/delete/<id>", methods=['POST', 'GET'])
@login_required
def process_delete(id):

    check_one = db.session.query(
        FabProc).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "Process deleted successfully"
        return redirect('/raw_materials')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/raw_materials')


# Raw Material Category  Edits

@app.route("/basic_master/cat/update/<id>", methods=['POST'])
@login_required
def cat_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    cat_form = RawCatForm()
    if cat_form.cat_update.data:
        cat_name = str(cat_form.cat.data)
        check_one = db.session.query(
            RawCat).filter_by(id=id).first()
        if check_one is not None:
            check_one.cat = cat_name
            check_one.desc = cat_form.desc.data
            db.session.commit()
            session['mssg'] = "Category updated successfully"
            return redirect('/raw_materials')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/raw_materials')


@app.route("/basic_master/cat/delete/<id>", methods=['POST', 'GET'])
@login_required
def cat_delete(id):

    check_one = db.session.query(
        RawCat).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "Category deleted successfully"
        return redirect('/raw_materials')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/raw_materials')


# Raw Material Width  Edits

@app.route("/basic_master/width/update/<id>", methods=['POST'])
@login_required
def width_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    width_form = FabWidthForm()
    if width_form.width_update.data:
        width_name = str(width_form.width.data)
        check_one = db.session.query(
            FabWidth).filter_by(id=id).first()
        if check_one is not None:
            check_one.width = width_name
            db.session.commit()
            session['mssg'] = "Width updated successfully"
            return redirect('/raw_materials')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/raw_materials')


@app.route("/basic_master/width/delete/<id>", methods=['POST', 'GET'])
@login_required
def width_delete(id):

    check_one = db.session.query(
        FabWidth).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "Width deleted successfully"
        return redirect('/raw_materials')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/raw_materials')


# Raw Material Dye  Edits

@app.route("/basic_master/dye/update/<id>", methods=['POST'])
@login_required
def dye_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    dye_form = FabDyeForm()
    if dye_form.dye_update.data:
        dye_name = str(dye_form.dye.data)
        check_one = db.session.query(
            FabDye).filter_by(id=id).first()
        if check_one is not None:
            check_one.dye = dye_name
            db.session.commit()
            session['mssg'] = "Dye updated successfully"
            return redirect('/raw_materials')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/raw_materials')


@app.route("/basic_master/dye/delete/<id>", methods=['POST', 'GET'])
@login_required
def dye_delete(id):

    check_one = db.session.query(
        FabDye).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "Dye deleted successfully"
        return redirect('/raw_materials')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/raw_materials')

# Raw Material Construction  Edits


@app.route("/basic_master/const/update/<id>", methods=['POST'])
@login_required
def const_edit(id):
    '''
        Edits data from the Data Display Table
        Requires Args :
        INPUT : item_id      
    '''
    const_form = FabConstForm()
    if const_form.const_update.data:
        const_name = str(const_form.const.data)
        check_one = db.session.query(
            FabConst).filter_by(id=id).first()
        if check_one is not None:
            check_one.const = const_name
            db.session.commit()
            session['mssg'] = "Construction updated successfully"
            return redirect('/raw_materials')
        else:
            session['mssg'] = "Something went wrong."
            return redirect('/raw_materials')


@app.route("/basic_master/const/delete/<id>", methods=['POST', 'GET'])
@login_required
def const_delete(id):

    check_one = db.session.query(
        FabConst).filter_by(id=id)
    if check_one.first() is not None:
        check_one.delete()
        db.session.commit()
        session['mssg'] = "Construction deleted successfully"
        return redirect('/raw_materials')
    else:
        session['mssg'] = "Something went wrong."
        return redirect('/raw_materials')

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
