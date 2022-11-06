from flask import Flask, flash, session, abort, render_template, request, url_for, redirect, jsonify, json, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import Column, ForeignKey, Integer, Table
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, IntegerField, SubmitField, FloatField, PasswordField, SelectField, TextAreaField, DateTimeLocalField
from wtforms.validators import InputRequired, EqualTo, Length, ValidationError, NumberRange
import bcrypt
import os
import random

#set app as a Flask instance
app = Flask(__name__)
#encryption relies on secret keys so they could be run
app.config['SECRET_KEY'] = os.urandom(12).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/hostel'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create the tables
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False) #To be HASHED
    role = db.Column(db.String(25), nullable=False)

    def __init__(self,email,password,role):
        self.email = email
        self.password = generate_password_hash(password) #HASHED
        self.role = role

class Students(db.Model):
    __tablename__ = 'student'
    grade_num = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    province = db.Column(db.String(20), nullable=False)
    postcode = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(15), nullable=False)
    category = db.Column(db.String(25), nullable=False)
    nationality = db.Column(db.String(25), nullable=False)
    special_needs = db.Column(db.Text, nullable=True)
    comments = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(10), nullable=False)
    major = db.Column(db.String(20), nullable=False)
    advisor_id = db.Column(db.Integer, ForeignKey('advisor.advisor_id'), nullable=False)    # many-to-one relationship
    advisor = db.relationship('Advisors', back_populates='student')

    def __init__(self,grade_num,fname,lname,address,city,province,postcode,dob,gender,category,nationality,special_needs,comments,status,major,advisor_id):
        self.grade_num = grade_num
        self.fname = fname
        self.lname = lname
        self.address = address
        self.city = city
        self.province = province
        self.postcode = postcode
        self.dob = dob
        self.gender = gender
        self.category = category
        self.nationality = nationality
        self.special_needs = special_needs
        self.comments = comments
        self.status = status
        self.major = major
        self.advisor_id = advisor_id

class Advisors(db.Model):
    __tablename__ = 'advisor'
    advisor_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    position = db.Column(db.String(25), nullable=False)
    department = db.Column(db.String(25), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    room_num = db.Column(db.Integer, nullable=False)
    staff_num = db.Column(db.Integer, ForeignKey('staff.staff_num'), nullable=False)
    student = db.relationship('Students', back_populates='advisor')
    staff = db.relationship('Staffs', back_populates='advisor')
    
    def __init__(self,advisor_id,fname,lname,position,department,phone,room_num,staff_num):
        self.advisor_id = advisor_id
        self.fname = fname
        self.lname = lname
        self.position = position
        self.department = department
        self.phone = phone
        self.room_num = room_num
        self.staff_num = staff_num

class Staffs(db.Model):
    __tablename__ = 'staff'
    staff_num = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    province = db.Column(db.String(20), nullable=False)
    postcode = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(15), nullable=False)
    position = db.Column(db.String(25), nullable=False)
    location = db.Column(db.String(25), nullable=False)
    advisor = db.relationship('Advisors', back_populates='staff', uselist=False)  # one-to-one relationship

    def __init__(self,staff_num,fname,lname,address,city,province,postcode,dob,gender,position,location):
        self.staff_num = staff_num
        self.fname = fname
        self.lname = lname
        self.address = address
        self.city = city
        self.province = province
        self.postcode = postcode
        self.dob = dob
        self.gender = gender
        self.position = position
        self.location = location


# Create the forms
class LoginForm(FlaskForm):
    email = StringField('Account Email', validators=[InputRequired(), Length(min=6, max=50)])
    password = PasswordField('Account Password', validators=[InputRequired(), Length(min=8, max=50)])
    submit = SubmitField('Login')

class StudentForm(FlaskForm):
    grade_num = IntegerField('Grade 12 Number', validators=[InputRequired(), NumberRange(min=10000000, max=99999999)])
    fname = StringField('First Name', validators=[InputRequired(), Length(min=2, max=25)])
    lname = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=25)])
    address = StringField('Address', validators=[InputRequired(), Length(min=5, max=50)])
    city = StringField(validators=[InputRequired(), Length(min=2, max=20)])
    province = StringField(validators=[InputRequired(), Length(min=2, max=20)])
    postcode = StringField(validators=[InputRequired(), Length(min=2, max=10)])
    dob = DateTimeLocalField('Date of Birth', format='%Y-%m-%d')
    gender = SelectField('Gender', choices=['Male', 'Female', 'Transgender'])
    category = SelectField('Category', choices=['First-Year Undergrad', 'Postgraduate'])
    nationality = StringField('Nationality', validators=[InputRequired(), Length(min=2, max=25)])
    special_needs = TextAreaField('Special Needs')
    comments = TextAreaField('Comments')
    status = SelectField('Status', choices=['Placed', 'Waiting'])
    major = StringField('Major', validators=[InputRequired(), Length(min=2, max=20)])
    advisor_id = IntegerField('Advisor ID', validators=[InputRequired(), NumberRange(min=10000, max=99999)])
    submit = SubmitField('Submit')

class AdvisorForm(FlaskForm):
    advisor_id = IntegerField('Advisor ID', validators=[InputRequired(), NumberRange(min=10000, max=99999)])
    fname = StringField('First Name', validators=[InputRequired(), Length(min=2, max=25)])
    lname = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=25)])
    position = SelectField('Position', choices=['Counsellor', 'Mentor', 'Guidance'])
    department = SelectField('Department', choices=['Arts', 'Economics', 'Education', 'Engineering', 'Humanities', 'Law', 'Music', 'Philosophy', 'Science'])
    phone = IntegerField('Internal Telephone Number', validators=[InputRequired()])
    room_num = IntegerField('Room Number', validators=[InputRequired(), NumberRange(min=100, max=9999)])
    staff_num = IntegerField('Staff Number', validators=[InputRequired(), NumberRange(min=100000, max=999999)])
    submit = SubmitField('Add Advisor')

class HallResForm(FlaskForm):
    hall_num = IntegerField('Hall Number')
    name = StringField('Hall Name')
    phone = StringField('Telephone Number')
    address = StringField('Address')
    manager = StringField('Manager')
    staff_num = IntegerField('Staff Number')
    capacity = IntegerField('Capacity')
    submit = SubmitField('Add Hall')

class HallRoomsForm(FlaskForm):
    place_num = IntegerField('Place Number')
    room_num = IntegerField('Room Number')
    rent = FloatField('Monthly Rent $')
    hall_name = StringField('Hall Name')
    hall_num = IntegerField('Hall Number')
    submit = SubmitField('Add Room')

class StuFlatsForm(FlaskForm):
    flat_num = IntegerField('Flat Number')
    address = StringField('Address')
    avail_room = IntegerField('Available Bedrooms')
    submit = SubmitField('Add Flat')

class FlatRoomsForm(FlaskForm):
    place_num = IntegerField('Place Number')
    room_num = IntegerField('Bedroom Number')
    rent = FloatField('Monthly Rent $')
    flat_num = IntegerField('Flat Number')
    submit = SubmitField('Add Bedroom')

class LeasesForm(FlaskForm):
    lease_num = IntegerField('Lease Number')
    semester = IntegerField('Number of Semesters')
    grade_num = IntegerField('Grade 12 Number')
    place_num = IntegerField('Place Number')
    room_num = IntegerField('Room Number')
    build_num = IntegerField('Hall/Flat Number')
    hostel = SelectField('Select Hostel', choices=['Residence Hall', 'Student Flats'])
    lease_start = DateTimeLocalField('Start Date', format='%Y-%m-%d')
    lease_end = DateTimeLocalField('End Date', format='%Y-%m-%d')
    submit = SubmitField('Add Lease')

class InvoicesForm(FlaskForm):
    invoice_num = IntegerField('Invoice Number')
    lease_num = IntegerField('Lease Number')
    semester = IntegerField('Number of Semesters')
    payment_due = FloatField('Payment Due $')
    grade_num = IntegerField('Grade 12 Number')
    place_num = IntegerField('Place Number')
    room_num = IntegerField('Room Number')
    build_num = IntegerField('Hall/Flat Number')
    hostel = SelectField('Select Hostel', choices=['Residence Hall', 'Student Flats'])
    payment_paid = FloatField('Payment Paid $')
    payment_date = DateTimeLocalField('Payment Date', format='%Y-%m-%d')
    payment_method = SelectField('Payment Method', choices=['Cheque', 'Cash'])
    first_reminder = DateTimeLocalField('First Reminder Date', format='%Y-%m-%d')
    second_reminder = DateTimeLocalField('Second Reminder Date', format='%Y-%m-%d')
    submit = SubmitField('Add Invoice')

class InspectForm(FlaskForm):
    inspect_num = IntegerField('Inspection Number')
    staff_num = IntegerField('Staff Number')
    fname = StringField('First Name')
    lname = StringField('Last Name')
    date = DateTimeLocalField('Inspection Date', format='%Y-%m-%d')
    satisfy = StringField('Satisfactory')
    comments = TextAreaField('Comments')
    flat_num = IntegerField('Flat Number')
    submit = SubmitField('Add Inspection')

class StaffForm(FlaskForm):
    staff_num = IntegerField('Staff Number', validators=[InputRequired(), NumberRange(min=100000, max=999999)])
    fname = StringField('First Name', validators=[InputRequired(), Length(min=2, max=25)])
    lname = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=25)])
    address = StringField('Address', validators=[InputRequired(), Length(min=5, max=50)])
    city = StringField(validators=[InputRequired(), Length(min=2, max=20)])
    province = StringField(validators=[InputRequired(), Length(min=2, max=20)])
    postcode = StringField(validators=[InputRequired(), Length(min=2, max=10)])
    dob = DateTimeLocalField('Date of Birth', format='%Y-%m-%d')
    gender = SelectField('Gender', choices=['Male', 'Female', 'Transgender'])
    position = SelectField('Position', choices=['Advisor', 'Flat Inspector', 'Hall Manager', 'Office Assistant'])
    location = SelectField('Location', choices=['Hostel Office', 'Hall', 'Flats'])
    submit = SubmitField('Add Staff')

class EditStaffForm(FlaskForm):
    fname = StringField('First Name')
    lname = StringField('Last Name')
    address = StringField('Address')
    city = StringField()
    province = StringField()
    postcode = StringField()
    dob = DateTimeLocalField('Date of Birth', format='%Y-%m-%d')
    gender = SelectField('Gender', choices=['Male', 'Female', 'Transgender'])
    position = SelectField('Position', choices=['Advisor', 'Flat Inspector', 'Hall Manager', 'Office Assistant'])
    location = SelectField('Location', choices=['Hostel Office', 'Hall', 'Flats'])
    submit = SubmitField('Edit Staff')

class SearchForm(FlaskForm):
    search_num = IntegerField('Search')
    search_type = SelectField('Type', choices=['Student Number', 'Advisor_ID', 'Staff Number'])
    submit = SubmitField('Search')

@app.route("/")
def index():
    session['admin'] = None
    return render_template('index.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if db.session.query(Admin).filter_by(email='admin@email.com').count() < 1:
        new_admin = Admin(email='admin@email.com', password='Admin+123', role='Administrator')
        db.session.add(new_admin)
        db.session.commit()
    
    if form.validate_on_submit():
        user = Admin.query.filter_by(email=form.email.data).first()
        if user:
            password = form.password.data #To be HASHED
            account = Admin.query.get(user.id)
            if check_password_hash(account.password,password):
                session['admin'] = account.email
                return redirect(url_for('dashboard'))
            else:
                flash('Incorrect Password')
        else:
            flash('Invalid email or password')
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    session['admin'] = None
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if session['admin'] is None:
        abort(403)
    return render_template('dashboard.html')

@app.route("/students", methods=["POST", "GET"])
def students():
    if session['admin'] is None:
        abort(403)
    form = StudentForm()
    if form.validate_on_submit():
        grade_num = form.grade_num.data
        fname = form.fname.data
        lname = form.lname.data
        address = form.address.data
        city = form.city.data
        province = form.province.data
        postcode = form.postcode.data
        dob = form.dob.data
        gender = form.gender.data
        category = form.category.data
        nationality = form.nationality.data
        status = form.status.data
        major = form.major.data
        advisor_id = form.advisor_id.data
        special_needs = form.special_needs.data
        comments = form.comments.data

        new_student = Students(grade_num,fname,lname,address,city,province,postcode,dob,gender,category,nationality,special_needs,comments,status,major,advisor_id)
        db.session.add(new_student)
        db.session.commit()
        flash(fname + ' ' + lname + ' is added as a new student')
        return redirect(url_for('students'))
    return render_template('students.html', form=form)

@app.route("/student_list", methods=["POST", "GET"])
def student_list():
    if session['admin'] is None:
        abort(403)
    students = Students.query.order_by(Students.grade_num.desc())
    return render_template('student_list.html', students=students)

@app.route("/advisors", methods=["POST", "GET"])
def advisors():
    if session['admin'] is None:
        abort(403)
    form = AdvisorForm()
    if form.validate_on_submit():
        advisor_id = form.advisor_id.data
        fname = form.fname.data
        lname= form.lname.data
        position = form.position.data
        department = form.department.data
        phone = form.phone.data
        room_num = form.room_num.data
        staff_num = form.staff_num.data

        new_advisor = Advisors(advisor_id,fname,lname,position,department,str(phone),room_num,staff_num)
        db.session.add(new_advisor)
        db.session.commit()
        flash(fname + ' ' + lname + ' is added as a new advisor')
        return redirect(url_for('advisors'))
    return render_template('advisors.html', form=form)

@app.route("/advisor_list", methods=["POST", "GET"])
def advisor_list():
    if session['admin'] is None:
        abort(403)
    advisors = Advisors.query.order_by(Advisors.advisor_id.desc())
    return render_template('advisor_list.html', advisors=advisors)

@app.route("/staffs", methods=["POST", "GET"])
def staffs():
    if session['admin'] is None:
        abort(403)
    form = StaffForm()
    if form.validate_on_submit():
        staff_num = form.staff_num.data
        fname = form.fname.data
        lname = form.lname.data
        address = form.address.data
        city = form.city.data
        province = form.province.data
        postcode= form.postcode.data
        dob = form.dob.data
        gender = form.gender.data
        position = form.position.data
        location = form.location.data

        new_staff = Staffs(staff_num,fname,lname,address,city,province,postcode,dob,gender,position,location)
        db.session.add(new_staff)
        db.session.commit()
        flash(fname + ' ' + lname + ' is added as a new staff')
        return redirect(url_for('staffs'))
    return render_template('staffs.html', form=form)

@app.route("/staff_list", methods=["POST", "GET"])
def staff_list():
    if session['admin'] is None:
        abort(403)
    staffs = Staffs.query.order_by(Staffs.staff_num.desc())
    return render_template('staff_list.html', staffs=staffs)

@app.route("/hall_res", methods=["POST", "GET"])
def hall_res():
    form = HallResForm()
    return render_template('hall_res.html', form=form)

@app.route("/hall_rooms", methods=["POST", "GET"])
def hall_rooms():
    form = HallRoomsForm()
    return render_template('hall_rooms.html', form=form)

@app.route("/stu_flats", methods=["POST", "GET"])
def stu_flats():
    form = StuFlatsForm()
    return render_template('stu_flats.html', form=form)

@app.route("/flat_rooms", methods=["POST", "GET"])
def flat_rooms():
    form = FlatRoomsForm()
    return render_template('flat_rooms.html', form=form)

@app.route("/leases", methods=["POST", "GET"])
def leases():
    form = LeasesForm()
    return render_template('leases.html', form=form)

@app.route("/invoices", methods=["POST", "GET"])
def invoices():
    form = InvoicesForm()
    return render_template('invoices.html', form=form)

@app.route("/inspections", methods=["POST", "GET"])
def inspections():
    form = InspectForm()
    return render_template('inspections.html', form=form)

@app.route("/search", methods=["POST", "GET"])
def search():
    form = SearchForm()
    return render_template('search.html', form=form)

@app.route('/staff_page')
def staff_page():
    return render_template('staff_page.html')

@app.route("/edit_staff", methods=["POST", "GET"])
def edit_staff():
    form = EditStaffForm()
    return render_template('edit_staff.html', form=form)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
