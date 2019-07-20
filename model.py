from wtforms import StringField, SelectField, FileField, SelectMultipleField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Optional
from flask_wtf import FlaskForm
from datetime import datetime
from flask_login import UserMixin
from wtforms_alchemy.fields import QuerySelectField ,SelectMultipleField ,SelectField
from wtforms.validators import InputRequired, Email, Length , DataRequired ,Regexp , Optional

from app import db


def uom_choice():
    return db.session.query(Uom)

class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')


class SignupForm(FlaskForm):
    username = StringField('username' , validators=[InputRequired()])
    password = PasswordField('password' ,  validators=[InputRequired()])
    email = StringField('email')

class UserForm(FlaskForm):
    username = StringField('username' ,  validators=[InputRequired()])
    password = PasswordField('password' , validators=[InputRequired()])
    submit = SubmitField('user_submit')
    update_submit = SubmitField('update_submit')

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer,  primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(250))
    roles = db.relationship('Role', secondary='user_roles')

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

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

#  Accessories & Form

class Accessories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acc = db.Column(db.String(50), unique=True, nullable=False)
    uom = db.relationship('Uom' ,cascade="all,delete", secondary='uom_acc' , backref='uom_acc' , lazy = 'joined')

db.Table('uom_acc',
    db.Column('uom_id' , db.Integer , db.ForeignKey('uom.id' , ondelete='SET NULL' )),
    db.Column('acc_id' , db.Integer , db.ForeignKey('accessories.id' , ondelete='SET NULL'))
)


class AccessoriesForm(FlaskForm):
    acc = StringField('acc', validators=[InputRequired()])
    uom = QuerySelectField('uom',validators=[InputRequired()] , query_factory= uom_choice , allow_blank= False  , get_label='measure')

    acc_submit = SubmitField('acc_submit')
    acc_update = SubmitField('acc_update')

#  Customer Category & Form

class OtherMat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mat = db.Column(db.String(50), unique=True, nullable=False)
    uom = db.relationship('Uom' ,cascade="all,delete", secondary='uom_oth' , backref='uom_oth' , lazy = 'joined')

db.Table('uom_oth',
    db.Column('uom_id' , db.Integer , db.ForeignKey('uom.id' , ondelete='SET NULL' )),
    db.Column('mat_id' , db.Integer , db.ForeignKey('other_mat.id' , ondelete='SET NULL'))
)

class OtherMatForm(FlaskForm):
    mat = StringField('mat', validators=[InputRequired()])
    uom = QuerySelectField('uom',validators=[InputRequired()] , query_factory= uom_choice , allow_blank= False  , get_label='measure')

    mat_submit = SubmitField('mat_submit')
    mat_update = SubmitField('mat_update')

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

# UOM Model & Form

class Uom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measure = db.Column(db.String(30), unique=True, nullable=False)
    desc = db.Column(db.String(250) , nullable= False)
    decimal = db.Column(db.Integer() , nullable= False)
    
class UomForm(FlaskForm):
    measure  = StringField('Measurement', validators=[InputRequired()])
    decimal = SelectField('decimal',validators=[InputRequired()] , choices=[('0','0') ,('1','1') ,('2','2') ,('3','3')])
    desc = StringField('Desciption')
    uom_submit = SubmitField('uom_submit')
    uom_update = SubmitField('uom_update') 

# Raw Material Master - Yarn Model & Form

class Yarn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    yarn = db.Column(db.String(30), unique=True, nullable=False)
    desc = db.Column(db.String(250) , nullable= False)

class YarnForm(FlaskForm):
    yarn  = StringField('Yarn', validators=[InputRequired()])
    desc = StringField('Desciption')
    yarn_submit = SubmitField('yarn_submit')
    yarn_update = SubmitField('yarn_update') 

# Fabric Construction Master
class FabConst(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    const = db.Column(db.String(30), unique=True, nullable=False)

class FabConstForm(FlaskForm):
    const  = StringField('Construction', validators=[InputRequired()])
    const_submit = SubmitField('const_submit')
    const_update = SubmitField('const_update') 

# Fabric Process Model & Form

class FabProc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    process = db.Column(db.String(30), unique=True, nullable=False)
    desc = db.Column(db.String(250) , nullable= False)

class FabProcForm(FlaskForm):
    proc  = StringField('Process', validators=[InputRequired()])
    desc = StringField('Desciption')
    proc_submit = SubmitField('proc_submit')
    proc_update = SubmitField('proc_update') 

# Fabric Width Master

class FabWidth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    width = db.Column(db.String(30), unique=True, nullable=False)

class FabWidthForm(FlaskForm):
    width  = StringField('Width', validators=[InputRequired()])
    width_submit = SubmitField('width_submit')
    width_update = SubmitField('width_update') 

# Fabric Dye Master

class FabDye(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dye = db.Column(db.String(30), unique=True, nullable=False)

class FabDyeForm(FlaskForm):
    dye  = StringField('Dye', validators=[InputRequired()])
    dye_submit = SubmitField('dye_submit')
    dye_update = SubmitField('dye_update') 


# Raw Material Category Model & Form

class RawCat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat = db.Column(db.String(30), unique=True, nullable=False)
    desc = db.Column(db.String(250) , nullable= False)

class RawCatForm(FlaskForm):
    cat  = StringField('Category', validators=[InputRequired()])
    desc = StringField('Desciption')
    cat_submit = SubmitField('cat_submit')
    cat_update = SubmitField('cat_update') 

############################################
############################################

# Fin Goods Product Category Model & Form

class FinCat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat = db.Column(db.String(30), unique=True, nullable=False)
    desc = db.Column(db.String(250) , nullable= False)

class FinCatForm(FlaskForm):
    cat  = StringField('Category', validators=[InputRequired()])
    desc = StringField('Desciption')
    cat_submit = SubmitField('cat_submit')
    cat_update = SubmitField('cat_update') 

# Raw Material Category Model & Form

class FabComb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comb = db.Column(db.String(30), unique=True, nullable=False)
    desc = db.Column(db.String(250) , nullable= False)

class FabCombForm(FlaskForm):
    comb  = StringField('Combination', validators=[InputRequired()])
    desc = StringField('Desciption')
    comb_submit = SubmitField('comb_submit')
    comb_update = SubmitField('comb_update') 

# Raw Material Category Model & Form

class PrintTech(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tech = db.Column(db.String(30), unique=True, nullable=False)
    desc = db.Column(db.String(250) , nullable= False)

class PrintTechForm(FlaskForm):
    tech  = StringField('Technique', validators=[InputRequired()])
    desc = StringField('Desciption')
    tech_submit = SubmitField('tech_submit')
    tech_update = SubmitField('tech_update') 

# Fin Design Master

class FinDes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    des = db.Column(db.String(30), unique=True, nullable=False)

class FinDesForm(FlaskForm):
    des  = StringField('Dye', validators=[InputRequired()])
    des_submit = SubmitField('des_submit')
    des_update = SubmitField('des_update') 


# Fin Size Master

class FinSize(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(30), unique=True, nullable=False)

class FinSizeForm(FlaskForm):
    size  = StringField('Dye', validators=[InputRequired()])
    size_submit = SubmitField('size_submit')
    size_update = SubmitField('size_update') 

# Main Master

# Finished Goods Choices 

def yarn_choice():
    return db.session.query(Yarn)

def fab_const_choice():
    return db.session.query(FabConst)

def fab_proc_choice():
    return db.session.query(FabProc)

def width_choice():
    return db.session.query(FabWidth)

def dye_choice():
    return db.session.query(FabDye)

def raw_cat_choice():
    return db.session.query(RawCat)

# Raw Material Fabric Choice 

def prod_cat_choice():
    return db.session.query(FinCat)

def fab_comb_choice():
    return db.session.query(FabComb)

def print_tech_choice():
    return db.session.query(PrintTech)

def design_choice():
    return db.session.query(FinDes)


# Finished Goods Master

class FinGoodsForm(FlaskForm):
    product_category = QuerySelectField('product_category',validators=[InputRequired()] , query_factory= prod_cat_choice , allow_blank= False  , get_label='cat')
    fabric_combo = QuerySelectField('fabric_combo',validators=[InputRequired()] , query_factory= fab_comb_choice , allow_blank= False  , get_label='comb')
    print_tech  = QuerySelectField('print_tech',validators=[InputRequired()] , query_factory= print_tech_choice , allow_blank= False  , get_label='tech')
    design = QuerySelectField('design',validators=[InputRequired()] , query_factory= design_choice , allow_blank= False  , get_label='des')
    uom = QuerySelectField('uom',validators=[InputRequired()] , query_factory= uom_choice , allow_blank= False  , get_label='measure')
    alt_name = StringField('alt_name')
    fin_submit = SubmitField('fin_submit')
    fin_update = SubmitField('fin_update')

class FinGoods(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    product_category = db.relationship('FinCat' ,cascade="all,delete", secondary='cat_goods' , backref='cat_goods' , lazy = 'joined')
    fabric_combo = db.relationship('FabComb' ,cascade="all,delete", secondary='comb_goods' , backref='comb_goods' , lazy = 'joined')
    print_tech = db.relationship('PrintTech' ,cascade="all,delete", secondary='tech_goods' , backref='print_goods' , lazy = 'joined')
    design = db.relationship('FinDes' ,cascade="all,delete", secondary='des_goods' , backref='des_goods' , lazy = 'joined')
    uom = db.relationship('Uom' ,cascade="all,delete", secondary='uom_goods' , backref='uom_goods' , lazy = 'joined')
    alt_name = db.Column(db.String(20))
    gen_name = db.Column(db.String(50))

    def get_gen_name(self):
        product_category = self.product_category
        fabric_combo = self.fabric_combo
        print_tech = self.print_tech
        design = self.design
        uom = self.uom
        display_name = "{} / {} / {} / {}".format(product_category[0].cat, fabric_combo[0].comb, print_tech[0].tech, design[0].des)
        return display_name

db.Table('cat_goods',
    db.Column('cat_id' , db.Integer , db.ForeignKey('fin_cat.id' , ondelete='SET NULL' )),
    db.Column('goods_id' , db.Integer , db.ForeignKey('fin_goods.id' , ondelete='SET NULL'))
)

db.Table('comb_goods',
    db.Column('comb_id' , db.Integer , db.ForeignKey('fab_comb.id' , ondelete='SET NULL' )),
    db.Column('goods_id' , db.Integer , db.ForeignKey('fin_goods.id' , ondelete='SET NULL'))
)
db.Table('tech_goods',
    db.Column('tech_id' , db.Integer , db.ForeignKey('print_tech.id' , ondelete='SET NULL' )),
    db.Column('goods_id' , db.Integer , db.ForeignKey('fin_goods.id' , ondelete='SET NULL'))
)
db.Table('des_goods',
    db.Column('des_id' , db.Integer , db.ForeignKey('fin_des.id' , ondelete='SET NULL' )),
    db.Column('goods_id' , db.Integer , db.ForeignKey('fin_goods.id' , ondelete='SET NULL'))
)
db.Table('uom_goods',
    db.Column('uom_id' , db.Integer , db.ForeignKey('uom.id' , ondelete='SET NULL' )),
    db.Column('goods_id' , db.Integer , db.ForeignKey('fin_goods.id' , ondelete='SET NULL'))
)

class RawFabMainForm(FlaskForm):
    product_category = QuerySelectField('product_category',validators=[InputRequired()] , query_factory= raw_cat_choice , allow_blank= False  , get_label='cat')
    yarn = QuerySelectField('yarn',validators=[InputRequired()] , query_factory= yarn_choice , allow_blank= False  , get_label='yarn')
    fab_const  = QuerySelectField('fab_const',validators=[InputRequired()] , query_factory= fab_const_choice , allow_blank= False  , get_label='const')
    proc = QuerySelectField('proc',validators=[InputRequired()] , query_factory= fab_proc_choice , allow_blank= False  , get_label='process')
    uom = QuerySelectField('uom',validators=[InputRequired()] , query_factory= uom_choice , allow_blank= False  , get_label='measure')
    width = QuerySelectField('width',validators=[InputRequired()] , query_factory= width_choice , allow_blank= False  , get_label='width')
    dye = QuerySelectField('dye',validators=[InputRequired()] , query_factory= dye_choice , allow_blank= False  , get_label='dye')
    alt_name = StringField('alt_name')
    raw_submit = SubmitField('raw_submit')
    raw_update = SubmitField('raw_update')


class RawFabMain(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    product_category = db.relationship('RawCat' ,cascade="all,delete", secondary='cat_fab_goods' , backref='cat_fab_goods' , lazy = 'joined')
    yarn = db.relationship('Yarn' ,cascade="all,delete", secondary='yarn_goods' , backref='yarn_goods' , lazy = 'joined')
    fab_const = db.relationship('FabConst' ,cascade="all,delete", secondary='const_goods' , backref='const_goods' , lazy = 'joined')
    proc = db.relationship('FabProc' ,cascade="all,delete", secondary='proc_goods' , backref='proc_goods' , lazy = 'joined')
    uom = db.relationship('Uom' ,cascade="all,delete", secondary='uom_raw_goods' , backref='uom_raw_goods' , lazy = 'joined')
    width = db.relationship('FabWidth' ,cascade="all,delete", secondary='width_goods' , backref='width_goods' , lazy = 'joined')
    dye = db.relationship('FabDye' ,cascade="all,delete", secondary='dye_goods' , backref='dye_goods' , lazy = 'joined')
    alt_name = db.Column(db.String(20))
    gen_name = db.Column(db.String(50))

    def get_gen_name(self):
        product_category = self.product_category
        yarn = self.yarn
        fab_const = self.fab_const
        proc = self.proc
        width = self.width
        dye = self.dye
        display_name = " {} / {} / {} / {}".format(product_category[0].cat, yarn[0].yarn ,fab_const[0].const, proc[0].process, width[0].width , dye[0].dye)
        return display_name
    

db.Table('cat_fab_goods',
    db.Column('cat_id' , db.Integer , db.ForeignKey('raw_cat.id' , ondelete='SET NULL' )),
    db.Column('raw_fab_id' , db.Integer , db.ForeignKey('raw_fab_main.id' , ondelete='SET NULL'))
)

db.Table('yarn_goods',
    db.Column('comb_id' , db.Integer , db.ForeignKey('yarn.id' , ondelete='SET NULL' )),
    db.Column('raw_fab_id' , db.Integer , db.ForeignKey('raw_fab_main.id' , ondelete='SET NULL'))
)
db.Table('const_goods',
    db.Column('const_id' , db.Integer , db.ForeignKey('fab_const.id' , ondelete='SET NULL' )),
    db.Column('raw_fab_id' , db.Integer , db.ForeignKey('raw_fab_main.id' , ondelete='SET NULL'))
)
db.Table('proc_goods',
    db.Column('proc_id' , db.Integer , db.ForeignKey('fab_proc.id' , ondelete='SET NULL' )),
    db.Column('raw_fab_id' , db.Integer , db.ForeignKey('raw_fab_main.id' , ondelete='SET NULL'))
)
db.Table('uom_raw_goods',
    db.Column('uom_id' , db.Integer , db.ForeignKey('uom.id' , ondelete='SET NULL' )),
    db.Column('raw_fab_id' , db.Integer , db.ForeignKey('raw_fab_main.id' , ondelete='SET NULL'))
)

db.Table('width_goods',
    db.Column('width_id' , db.Integer , db.ForeignKey('fab_width.id' , ondelete='SET NULL' )),
    db.Column('raw_fab_id' , db.Integer , db.ForeignKey('raw_fab_main.id' , ondelete='SET NULL'))
)

db.Table('dye_goods',
    db.Column('dye_id' , db.Integer , db.ForeignKey('fab_dye.id' , ondelete='SET NULL' )),
    db.Column('raw_fab_id' , db.Integer , db.ForeignKey('raw_fab_main.id' , ondelete='SET NULL'))
)

class Trans(db.Model):
    id = db.Column(db.Integer , primary_key= True)
    part_a = db.Column( db.JSON ,nullable =False , default = [] )
    part_b = db.Column( db.JSON ,nullable =False , default = [] )
    flag = db.Column( db.Integer , default = 0)
    meta=  db.Column( db.JSON , default = [])

from app import ma 

class TransSchema(ma.ModelSchema):
    class Meta:
        model = Trans