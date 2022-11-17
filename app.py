from flask import Flask, flash, session, abort, render_template, request, url_for, redirect, jsonify, json, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import Column, ForeignKey, Integer, Table
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, IntegerField, SubmitField, FloatField, PasswordField, SelectField, TextAreaField, DateTimeLocalField
from wtforms.validators import InputRequired, EqualTo, Length, ValidationError, NumberRange
import os
import random

#set app as a Flask instance
app = Flask(__name__)
#encryption relies on secret keys so they could be run
app.config['SECRET_KEY'] = os.urandom(12).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3307/hostel'
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
    lease_hall = db.relationship('LeasesHalls', back_populates='student')
    lease_flat = db.relationship('LeasesFlats', back_populates='student')

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
    department = db.Column(db.String(25), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    room_num = db.Column(db.Integer, nullable=False)
    staff_num = db.Column(db.Integer, ForeignKey('staff.staff_num'), nullable=False, unique=True)   # one-to-one relationship
    student = db.relationship('Students', back_populates='advisor')
    staff = db.relationship('Staffs', back_populates='advisor')
    
    def __init__(self,advisor_id,department,phone,room_num,staff_num):
        self.advisor_id = advisor_id
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
    advisor = db.relationship('Advisors', back_populates='staff')
    hallres = db.relationship('HallRes', back_populates='staff')
    inspector = db.relationship('Inspections', back_populates='staff')

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

class HallRes(db.Model):
    __tablename__ = 'hall_res'
    hall_num = db.Column(db.Integer, primary_key=True)
    hall_name = db.Column(db.String(25), nullable=False)
    hall_address = db.Column(db.String(50), nullable=False)
    hall_phone = db.Column(db.String(20), nullable=False)
    staff_num = db.Column(db.Integer, ForeignKey('staff.staff_num'), nullable=False, unique=True)
    capacity = db.Column(db.Integer, nullable=False)    # number of rooms in the hall
    staff = db.relationship('Staffs', back_populates='hallres')
    hallrooms = db.relationship('HallRooms', back_populates='hallnum')

    def __init__(self,hall_num,hall_name,hall_address,hall_phone,staff_num,capacity):
        self.hall_num = hall_num
        self.hall_name = hall_name
        self.hall_address = hall_address
        self.hall_phone = hall_phone
        self.staff_num = staff_num
        self.capacity = capacity

class HallRooms(db.Model):
    __tablename__ = 'hall_rooms'
    place_num = db.Column(db.Integer, primary_key=True) # identifies each room
    room_num = db.Column(db.Integer, nullable=False)    # each room has 1 student
    monthly_rent = db.Column(db.Float, nullable=False)
    hall_num = db.Column(db.Integer, ForeignKey('hall_res.hall_num'), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)    # only 1 spot in the room
    hallnum = db.relationship('HallRes', back_populates='hallrooms')
    lease_hall = db.relationship('LeasesHalls', back_populates='hallroom')

    def __init__(self,place_num,room_num,monthly_rent,hall_num,capacity):
        self.place_num = place_num
        self.room_num = room_num
        self.monthly_rent = monthly_rent
        self.hall_num = hall_num
        self.capacity = capacity

class StuFlats(db.Model):
    __tablename__ = 'stu_flats'
    flat_num = db.Column(db.Integer, primary_key=True)
    flat_address = db.Column(db.String(50), nullable=False)
    avail_room = db.Column(db.Integer, nullable=False)  # number of single bedrooms available
    flatrooms = db.relationship('FlatsRooms', back_populates='flatnum')
    inspector = db.relationship('Inspections', back_populates='flatnum')

    def __init__(self,flat_num,flat_address,avail_room):
        self.flat_num = flat_num
        self.flat_address = flat_address
        self.avail_room = avail_room

class FlatsRooms(db.Model):
    __tablename__ = 'flats_rooms'
    place_num = db.Column(db.Integer, primary_key=True) # identifies each room
    room_num = db.Column(db.Integer, nullable=False)    # each room has 3-5 students
    monthly_rent = db.Column(db.Float, nullable=False)
    flat_num = db.Column(db.Integer, ForeignKey('stu_flats.flat_num'), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)    # number of spots in the bedroom (3-5)
    flatnum = db.relationship('StuFlats', back_populates='flatrooms')
    lease_flat = db.relationship('LeasesFlats', back_populates='flatroom')

    def __init__(self,place_num,room_num,monthly_rent,flat_num,capacity):
        self.place_num = place_num
        self.room_num = room_num
        self.monthly_rent = monthly_rent
        self.flat_num = flat_num
        self.capacity = capacity

class LeasesHalls(db.Model):
    __tablename__ = 'leases_halls'
    lease_num = db.Column(db.Integer, primary_key=True) # each student has one room and one lease
    semester = db.Column(db.Integer, nullable=False)
    grade_num = db.Column(db.Integer, ForeignKey('student.grade_num'), nullable=False, unique=True)
    place_num = db.Column(db.Integer, ForeignKey('hall_rooms.place_num'), nullable=False, unique=True)
    lease_start = db.Column(db.Date, nullable=False)
    lease_end = db.Column(db.Date, nullable=True)
    student = db.relationship('Students', back_populates='lease_hall')
    hallroom = db.relationship('HallRooms', back_populates='lease_hall')
    invoice_hall = db.relationship('InvoicesHalls', back_populates='lease_hall')

    def __init__(self,lease_num,semester,grade_num,place_num,lease_start,lease_end):
        self.lease_num = lease_num
        self.semester = semester
        self.grade_num = grade_num
        self.place_num = place_num
        self.lease_start = lease_start
        self.lease_end = lease_end

class LeasesFlats(db.Model):
    __tablename__ = 'leases_flats'
    lease_num = db.Column(db.Integer, primary_key=True) # a bedroom can have up to 5 students and leases
    semester = db.Column(db.Integer, nullable=False)
    grade_num = db.Column(db.Integer, ForeignKey('student.grade_num'), nullable=False, unique=True) # each student has 1 lease
    place_num = db.Column(db.Integer, ForeignKey('flats_rooms.place_num'), nullable=False)
    lease_start = db.Column(db.Date, nullable=False)
    lease_end = db.Column(db.Date, nullable=True)
    student = db.relationship('Students', back_populates='lease_flat')
    flatroom = db.relationship('FlatsRooms', back_populates='lease_flat')
    invoice_flat = db.relationship('InvoicesFlats', back_populates='lease_flat')

    def __init__(self,lease_num,semester,grade_num,place_num,lease_start,lease_end):
        self.lease_num = lease_num
        self.semester = semester
        self.grade_num = grade_num
        self.place_num = place_num
        self.lease_start = lease_start
        self.lease_end = lease_end

class InvoicesHalls(db.Model):
    __tablename__ = 'invoices_halls'
    invoice_num = db.Column(db.Integer, primary_key=True)   # each lease has an invoice
    lease_num = db.Column(db.Integer, ForeignKey('leases_halls.lease_num'), nullable=False, unique=True)
    payment_due = db.Column(db.Float, nullable=False)
    payment_paid = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    payment_method = db.Column(db.String(30), nullable=False)
    first_reminder = db.Column(db.Date, nullable=True)
    second_reminder = db.Column(db.Date, nullable=True)
    lease_hall = db.relationship('LeasesHalls', back_populates='invoice_hall')

    def __init__(self,invoice_num,lease_num,payment_due,payment_paid,payment_date,payment_method,first_reminder,second_reminder):
        self.invoice_num = invoice_num
        self.lease_num = lease_num
        self.payment_due = payment_due
        self.payment_paid = payment_paid
        self.payment_date = payment_date
        self.payment_method = payment_method
        self.first_reminder = first_reminder
        self.second_reminder = second_reminder

class InvoicesFlats(db.Model):
    __tablename__ = 'invoices_flats'
    invoice_num = db.Column(db.Integer, primary_key=True)   # each lease has an invoice
    lease_num = db.Column(db.Integer, ForeignKey('leases_flats.lease_num'), nullable=False, unique=True)
    payment_due = db.Column(db.Float, nullable=False)
    payment_paid = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    payment_method = db.Column(db.String(30), nullable=False)
    first_reminder = db.Column(db.Date, nullable=True)
    second_reminder = db.Column(db.Date, nullable=True)
    lease_flat = db.relationship('LeasesFlats', back_populates='invoice_flat')

    def __init__(self,invoice_num,lease_num,payment_due,payment_paid,payment_date,payment_method,first_reminder,second_reminder):
        self.invoice_num = invoice_num
        self.lease_num = lease_num
        self.payment_due = payment_due
        self.payment_paid = payment_paid
        self.payment_date = payment_date
        self.payment_method = payment_method
        self.first_reminder = first_reminder
        self.second_reminder = second_reminder

class Inspections(db.Model):
    __tablename__ = 'inspection'
    inspect_num = db.Column(db.Integer, primary_key=True)
    staff_num = db.Column(db.Integer, ForeignKey('staff.staff_num'), nullable=False)
    flat_num = db.Column(db.Integer, ForeignKey('stu_flats.flat_num'), nullable=False)
    inspect_date = db.Column(db.Date, nullable=False)
    satisfy = db.Column(db.String(5), nullable=False)
    comments = db.Column(db.Text, nullable=True)
    staff = db.relationship('Staffs', back_populates='inspector')
    flatnum = db.relationship('StuFlats', back_populates='inspector')

    def __init__(self,inspect_num,staff_num,flat_num,inspect_date,satisfy,comments):
        self.inspect_num = inspect_num
        self.staff_num = staff_num
        self.flat_num = flat_num
        self.inspect_date = inspect_date
        self.satisfy = satisfy
        self.comments = comments

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
    status = SelectField('Status', choices=['Waiting', 'Placed'])
    major = StringField('Major', validators=[InputRequired(), Length(min=2, max=20)])
    advisor_id = IntegerField('Advisor ID', validators=[InputRequired(), NumberRange(min=10000, max=99999)])
    submit = SubmitField('Submit')

class AdvisorForm(FlaskForm):
    advisor_id = IntegerField('Advisor ID', validators=[InputRequired(), NumberRange(min=10000, max=99999)])
    department = SelectField('Department', choices=['Arts', 'Economics', 'Education', 'Engineering', 'Humanities', 'Law', 'Music', 'Philosophy', 'Science'])
    phone = IntegerField('Internal Telephone Number', validators=[InputRequired()])
    room_num = IntegerField('Room Number', validators=[InputRequired(), NumberRange(min=100, max=9999)])
    staff_num = IntegerField('Staff Number', validators=[InputRequired(), NumberRange(min=100000, max=999999)])
    submit = SubmitField('Add Advisor')

class HallResForm(FlaskForm):
    hall_num = IntegerField('Hall Number', validators=[InputRequired(), NumberRange(min=1, max=9)])
    hall_name = StringField('Hall Name', validators=[InputRequired(), Length(min=2, max=25)])
    address = StringField('Address', validators=[InputRequired(), Length(min=2, max=50)])
    phone = IntegerField('Telephone Number', validators=[InputRequired()])
    staff_num = IntegerField('Staff Number (Manager)', validators=[InputRequired(), NumberRange(min=100000, max=999999)])
    capacity = IntegerField('Capacity', validators=[InputRequired(), NumberRange(min=1, max=99)])
    submit = SubmitField('Add Hall')

class HallRoomsForm(FlaskForm):
    place_num = IntegerField('Place Number', validators=[InputRequired(), NumberRange(min=101, max=199)])
    room_num = IntegerField('Room Number', validators=[InputRequired(), NumberRange(min=101, max=199)])
    rent = FloatField('Monthly Rent $', validators=[InputRequired()])
    hall_num = IntegerField('Hall Number', validators=[InputRequired(), NumberRange(min=1, max=9)])
    submit = SubmitField('Add Room')

class StuFlatsForm(FlaskForm):
    flat_num = IntegerField('Flat Number', validators=[InputRequired(), NumberRange(min=1, max=9)])
    address = StringField('Address', validators=[InputRequired(), Length(min=2, max=50)])
    avail_room = IntegerField('Available Bedrooms', validators=[InputRequired(), NumberRange(min=1, max=30)])
    submit = SubmitField('Add Flat')

class FlatRoomsForm(FlaskForm):
    place_num = IntegerField('Place Number', validators=[InputRequired(), NumberRange(min=1001, max=1030)])
    room_num = IntegerField('Bedroom Number', validators=[InputRequired(), NumberRange(min=1001, max=1030)])
    rent = FloatField('Monthly Rent $', validators=[InputRequired()])
    flat_num = IntegerField('Flat Number', validators=[InputRequired(), NumberRange(min=1, max=9)])
    capacity = IntegerField('Number Of Beds', validators=[InputRequired(), NumberRange(min=3, max=5)])
    submit = SubmitField('Add Bedroom')

class LeasesForm(FlaskForm):
    lease_num = IntegerField('Lease Number', validators=[InputRequired()])    # building + place_num
    semester = IntegerField('Number of Semesters', validators=[InputRequired(), NumberRange(min=1, max=3)])
    grade_num = IntegerField('Grade 12 Number', validators=[InputRequired(), NumberRange(min=10000000, max=99999999)])
    place_num = IntegerField('Place Number', validators=[InputRequired()])
    hostel = SelectField('Select Hostel', choices=['Residence Hall', 'Student Flats'])
    lease_start = DateTimeLocalField('Start Date', format='%Y-%m-%d')
    lease_end = DateTimeLocalField('End Date', format='%Y-%m-%d')
    submit = SubmitField('Add Lease')

class InvoicesForm(FlaskForm):
    invoice_num = IntegerField('Invoice Number', validators=[InputRequired()])
    hostel = SelectField('Select Hostel', choices=['Residence Hall', 'Student Flats'])
    lease_num = IntegerField('Lease Number', validators=[InputRequired()])
    payment_due = FloatField('Payment Due $', validators=[InputRequired()])
    payment_paid = FloatField('Payment Paid $', validators=[InputRequired()])
    payment_date = DateTimeLocalField('Payment Date', format='%Y-%m-%d')
    payment_method = SelectField('Payment Method', choices=['N/A', 'Cheque', 'Cash', 'Debit Card', 'Online Banking', 'Money Order'])
    first_reminder = DateTimeLocalField('First Reminder Date', format='%Y-%m-%d')
    second_reminder = DateTimeLocalField('Second Reminder Date', format='%Y-%m-%d') # payment due date
    submit = SubmitField('Add Invoice')

class InspectForm(FlaskForm):
    inspect_num = IntegerField('Inspection Number', validators=[InputRequired(), NumberRange(min=10, max=999)])
    staff_num = IntegerField('Staff Number', validators=[InputRequired(), NumberRange(min=100000, max=999999)])
    flat_num = IntegerField('Flat Number', validators=[InputRequired(), NumberRange(min=1, max=9)])
    inspect_date = DateTimeLocalField('Inspection Date', format='%Y-%m-%d')
    satisfy = SelectField('Satisfactory', choices=['Yes', 'No'])
    comments = TextAreaField('Comments')
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
                return redirect(url_for('login'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

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
        advisor_id = form.advisor_id.data
        student_check = Students.query.filter_by(grade_num=grade_num).first()   # check the primary key
        advisor_check = Advisors.query.filter_by(advisor_id=advisor_id).first() # check the foreign key
        if student_check:
            flash('The student is already added', 'danger')
            return redirect(url_for('students'))
        elif not advisor_check:
            flash('The advisor does not exist', 'danger')
            return redirect(url_for('students'))
        else:
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
            special_needs = form.special_needs.data
            comments = form.comments.data

            new_student = Students(grade_num,fname,lname,address,city,province,postcode,dob,gender,category,nationality,special_needs,comments,status,major,advisor_id)
            db.session.add(new_student)
            db.session.commit()
            flash(fname + ' ' + lname + ' is added as a new student', 'success')
            return redirect(url_for('students'))
    return render_template('students.html', form=form)

@app.route("/student_list", methods=["POST", "GET"])
def student_list():
    if session['admin'] is None:
        abort(403)
    students = Students.query.order_by(Students.grade_num.desc())
    return render_template('student_list.html', students=students)

@app.route("/student_info/<acc>", methods=["POST", "GET"])
def student_info(acc):
    if session['admin'] is None:
        abort(403)
    student = Students.query.filter_by(grade_num=acc).first()
    advisor = Advisors.query.filter_by(advisor_id=student.advisor_id).first()
    staff = Staffs.query.filter_by(staff_num=advisor.staff_num).first()
    return render_template('student_info.html', student=student, staff=staff)

@app.route("/advisors", methods=["POST", "GET"])
def advisors():
    if session['admin'] is None:
        abort(403)
    form = AdvisorForm()
    if form.validate_on_submit():
        advisor_id = form.advisor_id.data
        staff_num = form.staff_num.data
        advisor_check = Advisors.query.filter_by(advisor_id=advisor_id).first() # check the primary key
        staff_check = Staffs.query.filter_by(staff_num=staff_num).first()   # check the foreign key
        staff_added = Advisors.query.filter_by(staff_num=staff_num).first() # check if the staff is already added
        if advisor_check:
            flash('The advisor is already added', 'danger')
            return redirect(url_for('advisors'))
        elif not staff_check:
            flash('The staff does not exist', 'danger')
            return redirect(url_for('advisors'))
        elif staff_check.position != "Advisor":
            flash('The staff is not an advisor', 'danger')
            return redirect(url_for('advisors'))
        elif staff_added:
            flash('The staff is already added as an advisor', 'danger')
            return redirect(url_for('advisors'))
        else:
            department = form.department.data
            phone = form.phone.data
            room_num = form.room_num.data

            new_advisor = Advisors(advisor_id,department,str(phone),room_num,staff_num)
            db.session.add(new_advisor)
            db.session.commit()
            flash(staff_check.fname + ' ' + staff_check.lname + ' is added as a new advisor', 'success')
            return redirect(url_for('advisors'))
    return render_template('advisors.html', form=form)

@app.route("/advisor_list", methods=["POST", "GET"])
def advisor_list():
    if session['admin'] is None:
        abort(403)
    advisors = Advisors.query.order_by(Advisors.advisor_id.desc())
    return render_template('advisor_list.html', advisors=advisors)

@app.route("/advisor_info/<acc>", methods=["POST", "GET"])
def advisor_info(acc):
    if session['admin'] is None:
        abort(403)
    advisor = Advisors.query.filter_by(advisor_id=acc).first()
    staff = Staffs.query.filter_by(staff_num=advisor.staff_num).first()
    return render_template('advisor_info.html', advisor=advisor, staff=staff)

@app.route("/staffs", methods=["POST", "GET"])
def staffs():
    if session['admin'] is None:
        abort(403)
    form = StaffForm()
    if form.validate_on_submit():
        staff_num = form.staff_num.data
        staff_check = Staffs.query.filter_by(staff_num=staff_num).first()   # check the primary key
        if staff_check:
            flash('The staff is already added', 'danger')
            return redirect(url_for('staffs'))
        else:
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
            flash(fname + ' ' + lname + ' is added as a new staff', 'success')
            return redirect(url_for('staffs'))
    return render_template('staffs.html', form=form)

@app.route("/staff_list", methods=["POST", "GET"])
def staff_list():
    if session['admin'] is None:
        abort(403)
    staffs = Staffs.query.order_by(Staffs.staff_num.desc())
    return render_template('staff_list.html', staffs=staffs)

@app.route("/staff_info/<acc>", methods=["POST", "GET"])
def staff_info(acc):
    if session['admin'] is None:
        abort(403)
    staff = Staffs.query.filter_by(staff_num=acc).first()
    return render_template('staff_info.html', staff=staff)

@app.route("/hall_res", methods=["POST", "GET"])
def hall_res():
    if session['admin'] is None:
        abort(403)
    form = HallResForm()
    if form.validate_on_submit():
        hall_num = form.hall_num.data
        staff_num = form.staff_num.data
        hall_check = HallRes.query.filter_by(hall_num=hall_num).first() # check the primary key
        staff_check = Staffs.query.filter_by(staff_num=staff_num).first()   # check the foreign key
        staff_added = HallRes.query.filter_by(staff_num=staff_num).first() # check if the staff is already added
        if hall_check:
            flash('The Hall Residence is already added', 'danger')
            return redirect(url_for('hall_res'))
        elif not staff_check:
            flash('The staff does not exist', 'danger')
            return redirect(url_for('hall_res'))
        elif staff_check.position != "Hall Manager":
            flash('The staff is not a Hall Manager', 'danger')
            return redirect(url_for('hall_res'))
        elif staff_added:
            flash('The staff is already added as a Hall Manager', 'danger')
            return redirect(url_for('hall_res'))
        else:
            hall_name = form.hall_name.data
            address = form.address.data
            phone = form.phone.data
            capacity = form.capacity.data

            new_hall = HallRes(hall_num,hall_name,address,str(phone),staff_num,capacity)
            db.session.add(new_hall)
            db.session.commit()
            flash('The ' + hall_name + ' Hall is added', 'success')
            return redirect(url_for('hall_res'))
    return render_template('hall_res.html', form=form)

@app.route("/hall_list", methods=["POST", "GET"])
def hall_list():
    if session['admin'] is None:
        abort(403)
    halls = HallRes.query.order_by(HallRes.hall_num.desc())
    return render_template('hall_list.html', halls=halls)

@app.route("/hall_info/<acc>", methods=["POST", "GET"])
def hall_info(acc):
    if session['admin'] is None:
        abort(403)
    hall = HallRes.query.filter_by(hall_num=acc).first()
    staff = Staffs.query.filter_by(staff_num=hall.staff_num).first()
    return render_template('hall_info.html', hall=hall, staff=staff)

@app.route("/hall_rooms", methods=["POST", "GET"])
def hall_rooms():
    if session['admin'] is None:
        abort(403)
    form = HallRoomsForm()
    if form.validate_on_submit():
        place_num = form.place_num.data
        hall_num = form.hall_num.data
        place_check = HallRooms.query.filter_by(place_num=place_num).first()    # check the primary key
        hall_check = HallRes.query.filter_by(hall_num=hall_num).first() # check the foreign key
        if place_check:
            flash('The Hall room is already added', 'danger')
            return redirect(url_for('hall_rooms'))
        elif not hall_check:
            flash('The Residence Hall does not exist', 'danger')
            return redirect(url_for('hall_rooms'))
        elif hall_check.capacity < 1:
            flash('The Residence Hall does not have any more rooms', 'danger')
            return redirect(url_for('hall_rooms'))
        else:
            room_num = form.room_num.data
            rent = form.rent.data
            capacity = 1

            hall_check.capacity = hall_check.capacity - 1
            new_room = HallRooms(place_num,room_num,rent,hall_num,capacity)
            db.session.add(new_room)
            db.session.commit()
            flash('A new Hall room is added', 'success')
            return redirect(url_for('hall_rooms'))
    return render_template('hall_rooms.html', form=form)

@app.route("/hroom_list", methods=["POST", "GET"])
def hroom_list():
    if session['admin'] is None:
        abort(403)
    one_rooms = HallRooms.query.filter_by(hall_num=1).order_by(HallRooms.place_num.desc())
    return render_template('hroom_list.html', one_rooms=one_rooms)

@app.route("/hroom_info/<acc>", methods=["POST", "GET"])
def hroom_info(acc):
    if session['admin'] is None:
        abort(403)
    hroom = HallRooms.query.filter_by(place_num=acc).first()
    hall = HallRes.query.filter_by(hall_num=hroom.hall_num).first()
    return render_template('hroom_info.html', hroom=hroom, hall=hall)

@app.route("/stu_flats", methods=["POST", "GET"])
def stu_flats():
    if session['admin'] is None:
        abort(403)
    form = StuFlatsForm()
    if form.validate_on_submit():
        flat_num = form.flat_num.data
        flat_check = StuFlats.query.filter_by(flat_num=flat_num).first()    # check the primary key
        if flat_check:
            flash('The Student Flat is already added', 'danger')
            return redirect(url_for('stu_flats'))
        else:
            address = form.address.data
            avail_room = form.avail_room.data

            new_flat = StuFlats(flat_num,address,avail_room)
            db.session.add(new_flat)
            db.session.commit()
            flash('A new Student Flat is added', 'success')
            return redirect(url_for('stu_flats'))
    return render_template('stu_flats.html', form=form)

@app.route("/flat_list", methods=["POST", "GET"])
def flat_list():
    if session['admin'] is None:
        abort(403)
    flats = StuFlats.query.order_by(StuFlats.flat_num.desc())
    return render_template('flat_list.html', flats=flats)

@app.route("/flat_info/<acc>", methods=["POST", "GET"])
def flat_info(acc):
    if session['admin'] is None:
        abort(403)
    flat = StuFlats.query.filter_by(flat_num=acc).first()
    return render_template('flat_info.html', flat=flat)

@app.route("/flat_rooms", methods=["POST", "GET"])
def flat_rooms():
    if session['admin'] is None:
        abort(403)
    form = FlatRoomsForm()
    if form.validate_on_submit():
        place_num = form.place_num.data
        flat_num = form.flat_num.data
        place_check = FlatsRooms.query.filter_by(place_num=place_num).first()    # check the primary key
        flat_check = StuFlats.query.filter_by(flat_num=flat_num).first()    # check the foreign key
        if place_check:
            flash('The Flat bedroom is already added', 'danger')
            return redirect(url_for('flat_rooms'))
        elif not flat_check:
            flash('The Student Flat does not exist', 'danger')
            return redirect(url_for('flat_rooms'))
        elif flat_check.avail_room < 1:
            flash('The Student Flat does not have any more bedrooms', 'danger')
            return redirect(url_for('flat_rooms'))
        else:
            room_num = form.room_num.data
            rent = form.rent.data
            capacity = form.capacity.data

            flat_check.avail_room = flat_check.avail_room - 1
            new_room = FlatsRooms(place_num,room_num,rent,flat_num,capacity)
            db.session.add(new_room)
            db.session.commit()
            flash('A new Flat bedroom is added', 'success')
            return redirect(url_for('flat_rooms'))
    return render_template('flat_rooms.html', form=form)

@app.route("/froom_list", methods=["POST", "GET"])
def froom_list():
    if session['admin'] is None:
        abort(403)
    one_rooms = FlatsRooms.query.filter_by(flat_num=1).order_by(FlatsRooms.place_num.desc())
    return render_template('froom_list.html', one_rooms=one_rooms)

@app.route("/froom_info/<acc>", methods=["POST", "GET"])
def froom_info(acc):
    if session['admin'] is None:
        abort(403)
    froom = FlatsRooms.query.filter_by(place_num=acc).first()
    flat = StuFlats.query.filter_by(flat_num=froom.flat_num).first()
    return render_template('froom_info.html', froom=froom, flat=flat)

@app.route("/leases", methods=["POST", "GET"])
def leases():
    if session['admin'] is None:
        abort(403)
    form = LeasesForm()
    if form.validate_on_submit():
        grade_num = form.grade_num.data
        hostel = form.hostel.data
        lease_num = form.lease_num.data
        place_num = form.place_num.data
        semester = form.semester.data
        lease_start = form.lease_start.data
        lease_end = form.lease_end.data
        student_check = Students.query.filter_by(grade_num=grade_num).first()   # check the foreign key
        if not student_check:
            flash('No available information on the student', 'danger')
            return redirect(url_for('leases'))
        elif student_check.status == "Placed":
            flash('The student is already placed', 'danger')
            return redirect(url_for('leases'))
        else:
            if hostel == "Residence Hall":
                lease_check = LeasesHalls.query.filter_by(lease_num=lease_num).first()  # check the primary key
                place_check = HallRooms.query.filter_by(place_num=place_num).first()
                if lease_check:
                    flash('The lease is already added', 'danger')
                    return redirect(url_for('leases'))
                elif not place_check:
                    flash('The hall room does not exist', 'danger')
                    return redirect(url_for('leases'))
                elif place_check.capacity < 1:
                    flash('The hall room is full', 'danger')
                    return redirect(url_for('leases'))
                else:
                    student_check.status = "Placed"
                    place_check.capacity = place_check.capacity - 1
                    new_lease = LeasesHalls(lease_num, semester, grade_num, place_num, lease_start, lease_end)
                    db.session.add(new_lease)
                    db.session.commit()
                    flash('A new lease in the Residence Hall room is added for the student', 'success')
                    return redirect(url_for('leases'))
            elif hostel == "Student Flats":
                lease_check = LeasesFlats.query.filter_by(lease_num=lease_num).first()  # check the primary key
                place_check = FlatsRooms.query.filter_by(place_num=place_num).first()
                if lease_check:
                    flash('The lease is already added', 'danger')
                    return redirect(url_for('leases'))
                elif not place_check:
                    flash('The flat bedroom does not exist', 'danger')
                    return redirect(url_for('leases'))
                elif place_check.capacity < 1:
                    flash('The flat bedroom is full', 'danger')
                    return redirect(url_for('leases'))
                else:
                    student_check.status = "Placed"
                    place_check.capacity = place_check.capacity - 1
                    new_lease = LeasesFlats(lease_num, semester, grade_num, place_num, lease_start, lease_end)
                    db.session.add(new_lease)
                    db.session.commit()
                    flash('A new lease in the Student Flat room is added for the student', 'success')
                    return redirect(url_for('leases'))
    return render_template('leases.html', form=form)

@app.route("/hall_leases", methods=["POST", "GET"])
def hall_leases():
    if session['admin'] is None:
        abort(403)
    leases = LeasesHalls.query.order_by(LeasesHalls.lease_num.desc())
    return render_template('hall_leases.html', leases=leases)

@app.route("/hall_lease/<acc>", methods=["POST", "GET"])
def hall_lease(acc):
    if session['admin'] is None:
        abort(403)
    lease = LeasesHalls.query.filter_by(lease_num=acc).first()
    student = Students.query.filter_by(grade_num=lease.grade_num).first()
    hroom = HallRooms.query.filter_by(place_num=lease.place_num).first()
    hall = HallRes.query.filter_by(hall_num=hroom.hall_num).first()
    return render_template('hall_lease.html', lease=lease, student=student, hroom=hroom, hall=hall)

@app.route("/flat_leases", methods=["POST", "GET"])
def flat_leases():
    if session['admin'] is None:
        abort(403)
    leases = LeasesFlats.query.order_by(LeasesFlats.lease_num.desc())
    return render_template('flat_leases.html', leases=leases)

@app.route("/flat_lease/<acc>", methods=["POST", "GET"])
def flat_lease(acc):
    if session['admin'] is None:
        abort(403)
    lease = LeasesFlats.query.filter_by(lease_num=acc).first()
    student = Students.query.filter_by(grade_num=lease.grade_num).first()
    froom = FlatsRooms.query.filter_by(place_num=lease.place_num).first()
    flat = StuFlats.query.filter_by(flat_num=froom.flat_num).first()
    return render_template('flat_lease.html', lease=lease, student=student, froom=froom, flat=flat)

@app.route("/invoices", methods=["POST", "GET"])
def invoices():
    if session['admin'] is None:
        abort(403)
    form = InvoicesForm()
    if form.validate_on_submit():
        hostel = form.hostel.data
        invoice_num = form.invoice_num.data
        lease_num = form.lease_num.data
        payment_due = form.payment_due.data
        payment_paid = form.payment_paid.data
        payment_date = form.payment_date.data
        payment_method = form.payment_method.data
        first_reminder = form.first_reminder.data
        second_reminder = form.second_reminder.data
        if hostel == "Residence Hall":
            invoice_check = InvoicesHalls.query.filter_by(invoice_num=invoice_num).first()    # check the primary key
            lease_check = LeasesHalls.query.filter_by(lease_num=lease_num).first()  # check the foreign key
            lease_added = InvoicesHalls.query.filter_by(lease_num=lease_num).first()  # check if the lease is already added
            if invoice_check:
                flash('The invoice is already added', 'danger')
                return redirect(url_for('invoices'))
            elif not lease_check:
                flash('The lease does not exist', 'danger')
                return redirect(url_for('invoices'))
            elif lease_added:
                flash('The lease is already added', 'danger')
                return redirect(url_for('invoices'))
            else:
                new_invoice = InvoicesHalls(invoice_num, lease_num, payment_due, payment_paid, payment_date, payment_method, first_reminder, second_reminder)
                db.session.add(new_invoice)
                db.session.commit()
                flash('A new invoice is added for the Residence Hall lease', 'success')
                return redirect(url_for('invoices'))
        elif hostel == "Student Flats":
            invoice_check = InvoicesFlats.query.filter_by(invoice_num=invoice_num).first()    # check the primary key
            lease_check = LeasesFlats.query.filter_by(lease_num=lease_num).first()  # check the foreign key
            lease_added = InvoicesFlats.query.filter_by(lease_num=lease_num).first()  # check if the lease is already added
            if invoice_check:
                flash('The invoice is already added', 'danger')
                return redirect(url_for('invoices'))
            elif not lease_check:
                flash('The lease does not exist', 'danger')
                return redirect(url_for('invoices'))
            elif lease_added:
                flash('The lease is already added', 'danger')
                return redirect(url_for('invoices'))
            else:
                new_invoice = InvoicesFlats(invoice_num, lease_num, payment_due, payment_paid, payment_date, payment_method, first_reminder, second_reminder)
                db.session.add(new_invoice)
                db.session.commit()
                flash('A new invoice is added for the Student Flat lease', 'success')
                return redirect(url_for('invoices'))
    return render_template('invoices.html', form=form)

@app.route("/hall_invoices", methods=["POST", "GET"])
def hall_invoices():
    if session['admin'] is None:
        abort(403)
    invoices = InvoicesHalls.query.order_by(InvoicesHalls.invoice_num.desc())
    return render_template('hall_invoices.html', invoices=invoices)

@app.route("/hall_invoice/<acc>", methods=["POST", "GET"])
def hall_invoice(acc):
    if session['admin'] is None:
        abort(403)
    invoice = InvoicesHalls.query.filter_by(invoice_num=acc).first()
    lease = LeasesHalls.query.filter_by(lease_num=invoice.lease_num).first()
    student = Students.query.filter_by(grade_num=lease.grade_num).first()
    hroom = HallRooms.query.filter_by(place_num=lease.place_num).first()
    hall = HallRes.query.filter_by(hall_num=hroom.hall_num).first()
    return render_template('hall_invoice.html', invoice=invoice, lease=lease, student=student, hroom=hroom, hall=hall)

@app.route("/flat_invoices", methods=["POST", "GET"])
def flat_invoices():
    if session['admin'] is None:
        abort(403)
    invoices = InvoicesFlats.query.order_by(InvoicesFlats.invoice_num.desc())
    return render_template('flat_invoices.html', invoices=invoices)

@app.route("/flat_invoice/<acc>", methods=["POST", "GET"])
def flat_invoice(acc):
    if session['admin'] is None:
        abort(403)
    invoice = InvoicesFlats.query.filter_by(invoice_num=acc).first()
    lease = LeasesFlats.query.filter_by(lease_num=invoice.lease_num).first()
    student = Students.query.filter_by(grade_num=lease.grade_num).first()
    froom = FlatsRooms.query.filter_by(place_num=lease.place_num).first()
    flat = StuFlats.query.filter_by(flat_num=froom.flat_num).first()
    return render_template('flat_invoice.html', invoice=invoice, lease=lease, student=student, froom=froom, flat=flat)

@app.route("/inspections", methods=["POST", "GET"])
def inspections():
    if session['admin'] is None:
        abort(403)
    form = InspectForm()
    if form.validate_on_submit():
        inspect_num = form.inspect_num.data
        staff_num = form.staff_num.data
        flat_num = form.flat_num.data
        inspect_check = Inspections.query.filter_by(inspect_num=inspect_num).first()    # check the primary key
        staff_check = Staffs.query.filter_by(staff_num=staff_num).first()
        flat_check = StuFlats.query.filter_by(flat_num=flat_num).first()
        if inspect_check:
            flash('The inspection number is already added', 'danger')
            return redirect(url_for('inspections'))
        elif not staff_check:
            flash('The staff does not exist', 'danger')
            return redirect(url_for('inspections'))
        elif staff_check.position != "Flat Inspector":
            flash('The staff is not a flat inspector', 'danger')
            return redirect(url_for('inspections'))
        elif not flat_check:
            flash('The student flat does not exist', 'danger')
            return redirect(url_for('inspections'))
        else:
            inspect_date = form.inspect_date.data
            satisfy = form.satisfy.data
            comments = form.comments.data

            new_inspect = Inspections(inspect_num, staff_num, flat_num, inspect_date, satisfy, comments)
            db.session.add(new_inspect)
            db.session.commit()
            flash('A new student flat inspection is added', 'success')
            return redirect(url_for('inspections'))
    return render_template('inspections.html', form=form)

@app.route("/inspect_list", methods=["POST", "GET"])
def inspect_list():
    if session['admin'] is None:
        abort(403)
    inspects = Inspections.query.order_by(Inspections.inspect_num.desc())
    return render_template('inspect_list.html', inspects=inspects)

@app.route("/inspect_info/<acc>", methods=["POST", "GET"])
def inspect_info(acc):
    if session['admin'] is None:
        abort(403)
    inspect = Inspections.query.filter_by(inspect_num=acc).first()
    staff = Staffs.query.filter_by(staff_num=inspect.staff_num).first()
    flat = StuFlats.query.filter_by(flat_num=inspect.flat_num).first()
    return render_template('inspect_info.html', inspect=inspect, staff=staff, flat=flat)

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

@app.route('/logout', methods=['GET'])
def logout():
    session['admin'] = None
    return redirect(url_for('index'))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
