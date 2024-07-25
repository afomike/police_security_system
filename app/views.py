import bcrypt
from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.forms import RegistrationForm, LoginForm, PoliceRecordForm, CaseForm
from app.models import User, PoliceRecord, Case
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.password.encode('utf-8')):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/add_record", methods=['GET', 'POST'])
@login_required
def add_record():
    form = PoliceRecordForm()
    if form.validate_on_submit():
        record = PoliceRecord(officer_name=form.officer_name.data, rank=form.rank.data, station=form.station.data, contact=form.contact.data)
        db.session.add(record)
        db.session.commit()
        flash('Police record has been added!', 'success')
        return redirect(url_for('view_records'))
    return render_template('add_record.html', title='Add Record', form=form)

@app.route("/view_records")
@login_required
def view_records():
    records = PoliceRecord.query.all()
    return render_template('view_records.html', title='View Records', records=records)

@app.route("/add_case", methods=['GET', 'POST'])
@login_required
def add_case():
    form = CaseForm()
    if form.validate_on_submit():
        case = Case(case_title=form.case_title.data, case_description=form.case_description.data, officer_id=form.officer_id.data)
        db.session.add(case)
        db.session.commit()
        flash('Case has been added!', 'success')
        return redirect(url_for('view_cases'))
    return render_template('add_case.html', title='Add Case', form=form)

@app.route("/view_cases")
@login_required
def view_cases():
    cases = Case.query.all()
    return render_template('view_cases.html', title='View Cases', cases=cases)

@app.route("/report")
@login_required
def report():
    report_data = db.session.query(Case.case_title, Case.case_description, PoliceRecord.officer_name).join(PoliceRecord).all()
    return render_template('report.html', title='Report', report=report_data)
