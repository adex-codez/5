from flask import Blueprint, render_template, redirect, url_for, flash, session
from . import db, bcrypt
from app.models import User, Patient, Doctor
from app.forms import RegistrationForm, LoginForm, UpdatePatientInfoForm,  UpdateDoctorInfoForm

main = Blueprint('main', __name__)

@main.route("/")
def home(): 
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    user = User.query.filter_by(id=session['user_id']).first()
    if user.user_type == 'Patient':
        return redirect(url_for('main.patient_dashboard'))
    else:    
        return redirect(url_for('main.doctor_dashboard'))

@main.route("/patient-dashboard")
def patient_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    return render_template('patient-dashboard.html')

@main.route("/doctor-dashboard")
def doctor_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    return render_template('doctor-dashboard.html')

@main.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password, user_type=form.user_type.data)
        
        if user.user_type == 'Patient':
            patient = Patient()
            user.patients.append(patient)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.patient_dashboard'))    
        else:
            doctor = Doctor()
            user.doctors.append(doctor)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.doctor_dashboard'))
        
    return render_template('register.html', form=form)

@main.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            if user.user_type == 'Patient':
                return redirect(url_for('main.patient_dashboard'))    
            else:
                return redirect(url_for('main.doctor_dashboard'))
        else:
            flash('Login Unsuccessful. Please check your email and password.', 'danger')
    return render_template('login.html', form=form)

@main.route("/logout")
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

@main.route("/patient/appointments")
def appointments():
    return render_template('appointments.html') 

@main.route("/patient/info")
def info():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    patient = Patient.query.filter_by(id=session['user_id']).first()
    return render_template('info.html', patient=patient)

@main.route("/patient/update-info", methods=['GET', 'POST'])
def update_patient_info():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    patient = Patient.query.filter_by(user_id=session['user_id']).first()
    if not patient:
        flash('Patient not found.', 'danger')
        return redirect(url_for('main.patient_dashboard'))
    form = UpdatePatientInfoForm(obj=patient)
    if form.validate_on_submit():
        patient.name = form.name.data
        patient.phone = form.phone.data
        patient.address = form.address.data
        patient.date_of_birth = form.date_of_birth.data
        patient.blood_group = form.blood_group.data
        patient.allergies = form.allergies.data
        patient.medical_history = form.medical_history.data
        db.session.commit()
        flash('Information Updated', 'success')
        return redirect(url_for('main.info'))
    return render_template('update-patient-info.html', form=form, patient=patient)


@main.route("/doctor/info")
def doctor_info():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    doctor = Doctor.query.filter_by(user_id=session['user_id']).first()
    print(doctor)
    return render_template('doctor-info.html', doctor=doctor)

@main.route("/doctor/update-info", methods=['GET', 'POST'])
def update_doctor_info():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    doctor = Doctor.query.filter_by(user_id=session['user_id']).first()
    if not doctor:
        flash('Doctor not found.', 'danger')
        return redirect(url_for('main.doctor_dashboard'))
    form = UpdateDoctorInfoForm(obj=doctor)
    if form.validate_on_submit():
        doctor.name = form.name.data
        doctor.phone = form.phone.data
        db.session.commit()
        flash('Information Updated', 'success')
        return redirect(url_for('main.doctor_info'))
    return render_template('update-doctor-info.html', form=form, doctor=doctor)

@main.route("/doctor/appointments")
def doctor_appointments():
    return render_template('appointments.html') 