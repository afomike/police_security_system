import bcrypt
from flask import render_template, url_for, flash, redirect, request
from app import app, db
import pandas as pd
from flask import Flask, render_template, request
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


def load_incompatible_model(filepath):
    import pickle
    with open(filepath, 'rb') as f:
        model = pickle.load(f, encoding='latin1')  # Use latin1 encoding to avoid certain compatibility checks
    return model

# model = load_incompatible_model('model/RF_model.pkl')

# # Load model and encoders
# model = joblib.load(f'model/RF_model.pkl')
# one_hot_encoder = joblib.load(f'model/one_hot_encoder.pkl')
# label_encoders = joblib.load(f'model/label_encoders.pkl')

# Define preprocessing function
# def preprocess_input(data):
#     df = pd.DataFrame(data, index=[0])
 
#     # Label Encoding for categorical features
#     label_encode_features = ['AREA NAME', 'Vict Sex']
#     for column in label_encode_features:
#         if column in df.columns:
#             le = label_encoders[column]
#             known_classes = set(le.classes_)
#             df[column] = df[column].apply(lambda x: le.transform([x])[0] if x in known_classes else -1)

#     # One-Hot Encoding for categorical features
#     one_hot_features = ['Weapon Desc', 'Status Desc']
#     if all(feature in df.columns for feature in one_hot_features):
#         one_hot_encoded = one_hot_encoder.transform(df[one_hot_features])
#         one_hot_encoded_df = pd.DataFrame(one_hot_encoded, columns=one_hot_encoder.get_feature_names_out(one_hot_features))

#         df = df.drop(columns=one_hot_features)
#         df = pd.concat([df.reset_index(drop=True), one_hot_encoded_df.reset_index(drop=True)], axis=1)

#     return df

# @app.route('/predict', methods=['GET', 'POST'])
# @login_required
# def predict():
#     if request.method == 'POST':
#         try:
#             data = request.form.to_dict()

#             # Check for required fields
#             required_fields = [
#                 'AREA', 'AREA NAME', 'Rpt Dist No', 'Part 1-2', 'Crm Cd', 'Crm Cd Desc',
#                 'Mocodes', 'Vict Age', 'Vict Sex', 'Premis Cd', 'Weapon Used Cd',
#                 'Weapon Desc', 'Status Desc', 'Crm Cd 1', 'Crm Cd 2', 'Crm Cd 3',
#                 'Crm Cd 4'
#             ]
            
#             missing_fields = [field for field in required_fields if field not in data]
#             if missing_fields:
#                 return render_template('index.html', prediction=f"Missing required fields: {', '.join(missing_fields)}")

#             preprocessed_data = preprocess_input(data)
#             prediction = model.predict(preprocessed_data)
#             prediction_result = prediction[0]
#             return render_template('index.html', prediction=f'Predicted Crime Category: {prediction_result}')
#         except Exception as e:
#             return render_template('index.html', prediction=f"Error: {str(e)}")

#     return render_template('prediction_form.html')
