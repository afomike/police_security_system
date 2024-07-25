from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class PoliceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    officer_name = db.Column(db.String(100), nullable=False)
    rank = db.Column(db.String(50), nullable=False)
    station = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(15), nullable=False)

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_title = db.Column(db.String(200), nullable=False)
    case_description = db.Column(db.Text, nullable=False)
    officer_id = db.Column(db.Integer, db.ForeignKey('police_record.id'), nullable=False)
