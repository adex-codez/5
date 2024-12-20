from app import db
from flask_sqlalchemy import SQLAlchemy
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_type = db.Column(db.String(60), nullable=False)
    
    

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    description = db.Column(db.String(120), nullable=False) 
    patient = db.relationship('Patient', back_populates='appointments', lazy=True)
    doctor = db.relationship('Doctor', back_populates='appointments', lazy=True)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    appointments = db.relationship('Appointment', back_populates='doctor', lazy=True)
    user = db.relationship('User', lazy=True)
    

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    blood_group = db.Column(db.String(120), nullable=False)
    allergies = db.Column(db.String(120), nullable=False)
    medical_history = db.Column(db.String(120), nullable=False)
    appointments = db.relationship('Appointment', back_populates='patient', lazy=True)
    user = db.relationship('User', lazy=True)