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
    staff_num = db.Column(db.Integer, ForeignKey('staff.staff_num'), nullable=False, unique=True)   # unique staff number
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
    hallres = db.relationship('HallRes', back_populates='staff', uselist=False)

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
    hall_manager = db.Column(db.String(25), nullable=False)
    staff_num = db.Column(db.Integer, ForeignKey('staff.staff_num'), nullable=False, unique=True)
    capacity = db.Column(db.Integer, nullable=False)    # number of rooms in the hall
    staff = db.relationship('Staffs', back_populates='hallres')
    hallrooms = db.relationship('HallRooms', back_populates='hallnum')

class HallRooms(db.Model):
    __tablename__ = 'hall_rooms'
    place_num = db.Column(db.Integer, primary_key=True) # identifies each room
    room_num = db.Column(db.Integer, nullable=False)    # each room has 1 student
    monthly_rent = db.Column(db.Float, nullable=False)
    hall_name = db.Column(db.String(25), nullable=False)
    hall_num = db.Column(db.Integer, ForeignKey('hall_res.hall_num'), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)    # only 1 spot in the room
    hallnum = db.relationship('HallRes', back_populates='hallrooms')

class StuFlats(db.Model):
    __tablename__ = 'stu_flats'
    flat_num = db.Column(db.Integer, primary_key=True)
    flat_address = db.Column(db.String(50), nullable=False)
    avail_room = db.Column(db.Integer, nullable=False)  # number of single bedrooms available
    flatrooms = db.relationship('FlatsRooms', back_populates='flatnum')

class FlatsRooms(db.Model):
    __tablename__ = 'flats_rooms'
    place_num = db.Column(db.Integer, primary_key=True) # identifies each room
    room_num = db.Column(db.Integer, nullable=False)    # each room has 3-5 students
    monthly_rent = db.Column(db.Float, nullable=False)
    flat_num = db.Column(db.Integer, ForeignKey('stu_flats.flat_num'), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)    # number of spots in the bedroom (3-5)
    flatnum = db.relationship('StuFlats', back_populates='flatrooms')


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
    hall_num = IntegerField('Hall Number', validators=[InputRequired(), NumberRange(min=1, max=10)])
    hall_name = StringField('Hall Name', validators=[InputRequired(), Length(min=2, max=25)])
    address = StringField('Address', validators=[InputRequired(), Length(min=2, max=50)])
    phone = IntegerField('Telephone Number', validators=[InputRequired()])
    manager = StringField('Manager', validators=[InputRequired(), Length(min=2, max=25)])
    staff_num = IntegerField('Staff Number', validators=[InputRequired(), NumberRange(min=100000, max=999999)])
    capacity = IntegerField('Capacity', validators=[InputRequired(), NumberRange(min=1, max=99)])
    submit = SubmitField('Add Hall')

class HallRoomsForm(FlaskForm):
    place_num = IntegerField('Place Number', validators=[InputRequired(), NumberRange(min=1, max=99)])
    room_num = IntegerField('Room Number', validators=[InputRequired(), NumberRange(min=1, max=99)])
    rent = FloatField('Monthly Rent $', validators=[InputRequired()])
    hall_name = StringField('Hall Name', validators=[InputRequired(), Length(min=2, max=25)])
    hall_num = IntegerField('Hall Number', validators=[InputRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField('Add Room')

class StuFlatsForm(FlaskForm):
    flat_num = IntegerField('Flat Number', validators=[InputRequired(), NumberRange(min=1, max=10)])
    address = StringField('Address', validators=[InputRequired(), Length(min=2, max=50)])
    avail_room = IntegerField('Available Bedrooms', validators=[InputRequired(), NumberRange(min=1, max=30)])
    submit = SubmitField('Add Flat')

class FlatRoomsForm(FlaskForm):
    place_num = IntegerField('Place Number', validators=[InputRequired(), NumberRange(min=1, max=30)])
    room_num = IntegerField('Bedroom Number', validators=[InputRequired(), NumberRange(min=1, max=30)])
    rent = FloatField('Monthly Rent $', validators=[InputRequired()])
    flat_num = IntegerField('Flat Number', validators=[InputRequired(), NumberRange(min=1, max=10)])
    capacity = IntegerField('Number Of Beds', validators=[InputRequired(), NumberRange(min=3, max=5)])
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
        elif staff_added:
            flash('The staff is already added as an advisor', 'danger')
            return redirect(url_for('advisors'))
        else:
            fname = form.fname.data
            lname= form.lname.data
            position = form.position.data
            department = form.department.data
            phone = form.phone.data
            room_num = form.room_num.data

            new_advisor = Advisors(advisor_id,fname,lname,position,department,str(phone),room_num,staff_num)
            db.session.add(new_advisor)
            db.session.commit()
            flash(fname + ' ' + lname + ' is added as a new advisor', 'success')
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
        elif staff_added:
            flash('The staff is already added as a Hall Manager', 'danger')
            return redirect(url_for('hall_res'))
        else:
            hall_name = form.hall_name.data
            address = form.address.data
            phone = form.phone.data
            manager = form.manager.data
            capacity = form.capacity.data

            new_hall = HallRes(hall_num,hall_name,address,phone,manager,staff_num,capacity)
            db.session.add(new_hall)
            db.session.commit()
            flash('The Hall ' + hall_name + ' is added', 'success')
            return redirect(url_for('hall_res'))
    return render_template('hall_res.html', form=form)

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
        else:
            room_num = form.room_num.data
            rent = form.rent.data
            hall_name = form.hall_name.data
            capacity = 1

            new_room = HallRooms(place_num,room_num,rent,hall_name,hall_num,capacity)
            db.session.add(new_room)
            db.session.commit()
            flash('A new Hall room is added', 'success')
            return redirect(url_for('hall_rooms'))
    return render_template('hall_rooms.html', form=form)

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
        else:
            room_num = form.room_num.data
            rent = form.rent.data
            capacity = form.capacity.data

            new_room = FlatsRooms(place_num,room_num,rent,flat_num,capacity)
            db.session.add(new_room)
            db.session.commit()
            flash('A new Flat bedroom is added', 'success')
            return redirect(url_for('flat_rooms'))
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

@app.route('/logout', methods=['GET'])
def logout():
    session['admin'] = None
    return redirect(url_for('index'))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
