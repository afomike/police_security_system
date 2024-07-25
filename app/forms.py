from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PoliceRecordForm(FlaskForm):
    officer_name = StringField('Officer Name', validators=[DataRequired()])
    rank = StringField('Rank')
    station = StringField('Station')
    contact = StringField('Contact')
    submit = SubmitField('Add Record')

class CaseForm(FlaskForm):
    case_title = StringField('Case Title', validators=[DataRequired()])
    case_description = TextAreaField('Case Description')
    officer_id = StringField('Officer ID', validators=[DataRequired()])
    submit = SubmitField('Add Case')
