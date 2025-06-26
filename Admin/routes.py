from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, fresh_login_required
from Models.base_model import db, get_local_time
from Models.users import Patients, PatientAddress
from Models.medicine import Medicine
from Models.diseases import Disease
from Models.payment import Payment
from Models.lab_analysis import LabAnalysis, LabAnalysisDetails
from Models.appointment import Appointment
from Models.prescription import Prescription, PrescriptionDetails
from Models.diagnosis import Diagnosis, DiagnosisDetails
from .form import AddPatientForm, DiagnosisForm, PrescriptionForm, LabAnalysisForm, AddDiseaseForm, AddMedicineForm
from Documents.export_pdf import generate_payment_pdf
from decorator import role_required
from collections import Counter
import folium
import pandas as pd
from sqlalchemy.sql import func, cast, literal_column
from sqlalchemy.types import String

admin = Blueprint("admin", __name__)

@admin.route("/")
@admin.route("/home")
@login_required
def home():
  patients = Patients.query.all()
  medicines = Medicine.query.all()
  appointments = Appointment.query.all()
  client_medicines = Prescription.query.all()
  payments = Payment.query.all()
  diseases = Disease.query.all()
  diagnosis = Diagnosis.query.all()
  prescriptions = Prescription.query.all()

  diagnosis_disease_ids = [diagnosis for diagnosis in db.session.query(DiagnosisDetails.disease_id, func.count(DiagnosisDetails.disease_id).label('count')).group_by(DiagnosisDetails.disease_id).order_by(func.count(DiagnosisDetails.disease_id).desc()).limit(limit=5).all()]

  prescription_medicine_ids = [prescription for prescription in db.session.query(PrescriptionDetails.medicine_id, func.count(PrescriptionDetails.medicine_id).label('count')).group_by(PrescriptionDetails.medicine_id).order_by(func.count(PrescriptionDetails.medicine_id).desc()).limit(limit=5).all()]

  context = {
    "patients": patients,
    "client_medicines" : client_medicines, 
    "payments" : payments,
    "medicines" : medicines,
    "diseases" : diseases,
    "all_diagnosis" : diagnosis,
    "prescriptions" : prescriptions,
    "appointments" : appointments,
    "lab_tests" : LabAnalysis.query.all(),
    "diagnosis_disease_ids": diagnosis_disease_ids,
    "prescription_medicine_ids": prescription_medicine_ids,
  }
  
  return render_template("Main/home.html", **context)

@admin.route("/find-patient/<string:search_text>")
def patient_search(search_text):
  patients = Patients.query.filter(Patients.first_name.like("%" + search_text.capitalize() + "%")).all()
  
  patients_count = Patients.query.filter(Patients.first_name.like("%" + search_text.capitalize() + "%")).count()

  patients_list = [
    {
      "unique_id": patient.unique_id,
      "name": f"{patient.first_name} {patient.last_name}",
      "gender": patient.gender.capitalize(),
      "count": patients_count,
    } 
    for patient in patients
  ]

  return jsonify(patients_list)

@admin.route("/map")
def render_map():
  try:
    return render_template("tanzania_map.html")
  except:
    return "No data to display on the map"

@admin.route("/add/medicine", methods=["POST", "GET"])
@login_required
def add_medicine():
  form = AddMedicineForm()
  if form.validate_on_submit():
    try:
      new_medicine = Medicine(
        name = form.name.data,
        price = form.price.data,
        quantity = form.quantity.data,
      )
      db.session.add(new_medicine)
      db.session.commit()
      flash('Medicine added successfully!', 'success')
      return redirect(url_for('admin.home'))
        
    except Exception as e:
      db.session.rollback()
      flash('Error adding medicine: ' + str(e), 'danger')
      return redirect(url_for('admin.add_medicine'))
  
  context = {
    "form": form
  }

  return render_template("Main/add-medicine.html", **context)

@admin.route("/edit/medicine/<int:medicine_id>", methods=["POST", "GET"])
@login_required
def edit_medicine(medicine_id):
  medicine = Medicine.query.filter_by(unique_id=medicine_id).first()
  if not medicine:
    flash("Medicine not found", category="danger")
    return redirect(url_for("admin.home"))
  
  form = AddMedicineForm(obj=medicine)

  if form.validate_on_submit():
    try:
      medicine.name = form.name.data
      medicine.price = form.price.data
      if form.quantity.data:
        medicine.quantity = medicine.quantity + form.quantity.data
      db.session.commit()
      flash("Medicine updated successfully", "success")
      return redirect(url_for("admin.edit_medicine", medicine_id=medicine.unique_id))
    except Exception as e:
      flash(f"Error: {str(e)}", "danger")
      return redirect(url_for("admin.edit_medicine", medicine_id=medicine.unique_id))

  context = {
    "form": form,
    "title_message": "Edit"
  }

  return render_template("Main/add-medicine.html", **context)

@admin.route("/remove/medicine/<int:medicine_id>")
@login_required
def remove_medicine(medicine_id):
  medicine = Medicine.query.filter_by(unique_id=medicine_id).first()
  if not medicine:
    flash("Medicine not found", category="danger")
    return redirect(url_for("admin.home"))
  
  try:
    db.session.delete(medicine)
    db.session.commit()
    flash("Medicine removed successfully", "success")
  except Exception as e:
    flash(f"Error: {str(e)}", "danger")

  return redirect(url_for('admin.home'))

@admin.route("/add/disease", methods=["POST", "GET"])
@login_required
def add_disease():
  form = AddDiseaseForm()
  if form.validate_on_submit():
    try:
      new_disease = Disease(
        name = form.name.data,
      )
      db.session.add(new_disease)
      db.session.commit()
      flash('Disease added successfully!', 'success')
      return redirect(url_for('admin.home'))
        
    except Exception as e:
      db.session.rollback()
      flash('Error adding medicine: ' + str(e), 'danger')
      return redirect(url_for('admin.add_disease'))
  
  context = {
    "form": form
  }

  return render_template("Main/add-disease.html", **context)

@admin.route("/edit/disease/<int:disease_id>", methods=["POST", "GET"])
@login_required
def edit_disease(disease_id):
  disease = Disease.query.filter_by(unique_id=disease_id).first()
  if not disease:
    flash("Disease not found", category="danger")
    return redirect(url_for("admin.home"))
  
  form = AddMedicineForm(obj=disease)

  if form.validate_on_submit():
    try:
      form.populate_obj(disease)
      db.session.commit()
      flash("Disease updated successfully", "success")
      return redirect(url_for("admin.edit_disease", disease_id=disease.unique_id))
    except Exception as e:
      flash(f"Error: {str(e)}", "danger")
      return redirect(url_for("admin.edit_disease", disease_id=disease.unique_id))

  context = {
    "form": form,
    "title_message": "Edit"
  }

  return render_template("Main/add-disease.html", **context)

@admin.route("/remove/disease/<int:disease_id>")
@login_required
def remove_disease(disease_id):
  disease = Disease.query.filter_by(unique_id=disease_id).first()
  if not disease:
    flash("Disease not found", category="danger")
    return redirect(url_for("admin.home"))
  
  try:
    db.session.delete(disease)
    db.session.commit()
    flash("Disease removed successfully", "success")
  except Exception as e:
    flash(f"Error: {str(e)}", "danger")

  return redirect(url_for('admin.home'))

@admin.route("/add/patient", methods=["POST", "GET"])
@login_required
def add_patient():
  form = AddPatientForm()
  if form.validate_on_submit():
    try:
      patient = Patients(
        first_name = form.first_name.data,
        last_name = form.last_name.data,
        age = form.age.data,
        gender = form.gender.data,
        phone_number_1 = form.phone_number_1.data,
        phone_number_2 = form.phone_number_2.data
      )
      db.session.add(patient)
      db.session.flush()
      if form.region.data or form.district.data:
        address = PatientAddress(
          region = form.region.data,
          district = form.district.data,
          patient_id = patient.id
        )
        db.session.add(address)
      
      db.session.commit()
      flash('Patient created successfully!', 'success')
      return redirect(url_for('admin.home'))
        
    except Exception as e:
      db.session.rollback()
      flash('Error creating patient: ' + str(e), 'danger')
      return redirect(url_for('admin.add_patient'))
  
  context = {
    "form": form
  }

  return render_template("Main/add-patient.html", **context)

@admin.route("/edit/patient/<int:patient_id>", methods=["POST", "GET"])
@login_required
def edit_patient(patient_id):
  patient = Patients.query.filter_by(unique_id = patient_id).first()
  if not patient:
    flash("Patient not found", "danger")
    return redirect(url_for("admin.home"))
  
  patient_address = PatientAddress.query.filter_by(patient_id=patient.id).first()

  form_data = {}
  form_data.update(patient.to_dict())
  if patient_address:
    form_data.update(patient_address.to_dict())
    
  form = AddPatientForm(data=form_data)

  if form.validate_on_submit():
    try:
      form.populate_obj(patient)
      if patient_address:
        form.populate_obj(patient_address)
      else:
        address = PatientAddress(
          region = form.region.data,
          district = form.district.data,
          patient_id = patient.id
        )
        db.session.add(address)
      db.session.commit()
      flash("Patient details updated successfully", "success")
    except Exception as e:
      flash(f"Error submitting form: {str(e)}", "danger")

    return redirect(url_for("admin.edit_patient", patient_id=patient.unique_id))

  context = {
    "patient": patient,
    "form": form,
    "title_message": "Edit"
  }

  return render_template("Main/add-patient.html", **context)

@admin.route("/remove-patient/<int:patient_id>")
@login_required
def remove_patient(patient_id):
  patient = Patients.query.filter_by(unique_id = patient_id).first()
  if not patient:
    flash("Patient not found", "danger")
    return redirect(url_for("admin.home"))
  db.session.delete(patient)
  db.session.commit()
  flash("Patient removed successfully", "success")
  return redirect(url_for('admin.home'))

@admin.route("/profile/patient/<int:patient_id>")
@login_required
def patient_profile(patient_id):
  patient = Patients.query.filter_by(unique_id = patient_id).first()
  if not patient:
    flash("Patient not found", "danger")
    return redirect(url_for("admin.home"))

  patient_address = PatientAddress.query.filter_by(patient_id=patient.id).first()
  patient_lab_analysis = LabAnalysis.query.filter_by(patient_id=patient.id).all()
  patient_prescriptions = Prescription.query.filter_by(patient_id=patient.id).all()
  patient_payments = Payment.query.filter_by(patient_id=patient.id).all()
  patient_apointments = Appointment.query.filter_by(patient_id=patient.id).all()

  context = {
    "patient": patient,
    "patient_address": patient_address,
    "patient_lab_analysis": patient_lab_analysis,
    "patient_prescriptions": patient_prescriptions,
    "patient_payments": patient_payments,
    "patient_appointments": patient_apointments,
  }

  return render_template('Main/patient-profile.html', **context)

@admin.route("/create-appointment/<int:patient_id>")
@login_required
@role_required(["Admin", "Lab Tech", "Clerk"])
def create_appointment(patient_id):
  patient = Patients.query.filter_by(unique_id=patient_id).first()
  if not patient:
    flash("Failed to create appointment, patient not found", "danger")
    return redirect(url_for("admin.home"))
  
  existing_appointment = Appointment.query.filter_by(patient_id=patient.id, is_active=True).first()

  if not existing_appointment:
    new_appointment = Appointment(
      patient_id = patient.id
    )
    db.session.add(new_appointment)
    db.session.commit()
    return redirect(url_for("admin.appointment", appointment_id=new_appointment.unique_id))

  return redirect(url_for("admin.appointment", appointment_id=existing_appointment.unique_id))

@admin.route("/appointment/<int:appointment_id>")
@login_required
@role_required(["Admin", "Lab Tech", "Clerk"])
def appointment(appointment_id):
  appointment = Appointment.query.filter_by(unique_id=appointment_id).first()
  if not appointment:
    flash("Appointment not found", "danger")
    return redirect(url_for("admin.home"))
  
  patient = Patients.query.filter_by(id=appointment.patient_id).first()

  lab_analysis = LabAnalysis.query.filter_by(appointment_id=appointment.id).all()

  diagnosis = Diagnosis.query.filter_by(appointment_id=appointment.id).first()
  if diagnosis:
    diagnosis_form = DiagnosisForm(obj=diagnosis)
    diagnosis_details = DiagnosisDetails.query.filter_by(diagnosis_id=diagnosis.id).all()
  else:
    diagnosis_form = DiagnosisForm()
    diagnosis_details = []

  prescription = Prescription.query.filter_by(appointment_id=appointment.id).first()
  if prescription:
    prescription_form = PrescriptionForm(obj=prescription)
    prescription_details = PrescriptionDetails.query.filter_by(prescription_id=prescription.id).all()
  else:
    prescription_form = PrescriptionForm()
    prescription_details = []

  context = {
    "appointment": appointment,
    "lab_analysis": lab_analysis,
    "patient": patient,
    "diagnosis": diagnosis,
    "diagnosis_details": diagnosis_details,
    "lab_analysis_form": LabAnalysisForm(),
    "diagnosis_form": diagnosis_form,
    "prescription_form": prescription_form,
    "prescription_details": prescription_details,
    "diseases": Disease.query.all(),
    "medicines": Medicine.query.all(),
  }

  return render_template("Main/appointment.html", **context)

@admin.route("/lab-analysis/<int:appointment_id>", methods=["POST"])
@login_required
@role_required(["Admin", "Clerk"])
def add_lab_analysis(appointment_id):
  appointment = Appointment.query.filter_by(unique_id=appointment_id).first()
  if not appointment:
    flash("Appointment not found", "danger")
    return redirect(url_for("admin.home"))

  if appointment.is_active == False:
    flash("Appointment is not active", "warning")
    return redirect(url_for("admin.appointment", appointment_id=appointment.unique_id))

  form = LabAnalysisForm()

  try:
    existing_lab_analysis = LabAnalysis.query.filter_by(appointment_id=appointment.id, is_active=True).first()
    if not existing_lab_analysis:
      new_lab_analysis = LabAnalysis(
        patient_id = appointment.patient_id,
        appointment_id = appointment.id,
      )
      db.session.add(new_lab_analysis)
      db.session.flush()
      create_lab_analysis_details(new_lab_analysis.id, form)
    else:
      create_lab_analysis_details(existing_lab_analysis.id, form)
    db.session.commit()
    flash("Lab Test Submitted Successfully", "success")
  except Exception as e:
    db.session.rollback()
    flash(f"Error: {str(e)}", "danger")

  return redirect(url_for("admin.appointment", appointment_id=appointment.unique_id))

def create_lab_analysis_details(lab_analysis_id, form):
  new_lab_detail = LabAnalysisDetails(
    lab_analysis_id = lab_analysis_id,
    test = form.test.data,       
    result = form.result.data,       
  )
  db.session.add(new_lab_detail)

@admin.route("/remove-lab-test/<int:lab_analysis_id>")
@login_required
@role_required(["Admin", "Lab Tech"])
def remove_lab_analysis(lab_analysis_id):
  lab_analysis = LabAnalysisDetails.query.filter_by(unique_id=lab_analysis_id).first()
  if not lab_analysis:
    flash("Lab test not found", "danger")
    return redirect(request.referrer)
  try:
    db.session.delete(lab_analysis)
    db.session.commit()
    flash("Lab test removed successfully", "success")
    return redirect(request.referrer)
  except Exception as e:
    flash(f"{repr(e)}", "danger")
    return redirect(request.referrer)

@admin.route("/approve/lab-analysis/<int:lab_analysis_id>")
@login_required
@role_required(["Admin", "Lab Tech"])
def approve_lab_analysis(lab_analysis_id):
  lab_analysis = LabAnalysis.query.filter_by(unique_id=lab_analysis_id).first()
  if not lab_analysis:
    flash("Lab analysis not found", "danger")
    return redirect(url_for("admin.home"))
  if lab_analysis.is_approved:
    flash("Lab analysis already approved", "info")
    return redirect(url_for("admin.appointment", appointment_id=lab_analysis.appointment_lab_analysis.unique_id))
  try:
    appointment = Appointment.query.filter_by(id=lab_analysis.appointment_id).first()
    lab_analysis.is_active = False
    lab_analysis.is_approved = True
    lab_analysis.date_approved = get_local_time()
    db.session.commit()
    flash("Lab Test approved Successfully", "success")
  except Exception as e:
    flash(f"Error: {str(e)}", "danger")
    return redirect(url_for(request.referrer))

  return redirect(url_for("admin.appointment", appointment_id=appointment.unique_id))

@admin.route("/diagnose/patient/<int:appointment_id>", methods=["POST"])
@login_required
@role_required(["Admin", "Lab Tech"])
def add_diagnosis(appointment_id):
  appointment = Appointment.query.filter_by(unique_id=appointment_id).first()
  if not appointment:
    flash("Appointment not found", "danger")
    return redirect(url_for("admin.home"))
  
  if appointment.is_active == False:
    flash("Appointment is not active", "warning")
    return redirect(url_for("admin.appointment", appointment_id=appointment.unique_id))

  form = DiagnosisForm()

  try:
    diseases_ids = request.form.getlist("diseases")
    patient = Patients.query.get(appointment.patient_id)
    existing_diagnosis = Diagnosis.query.filter_by(appointment_id=appointment.id, patient_id=patient.id, is_active=True).first()
    if not existing_diagnosis:
      new_diagnosis = Diagnosis(
        patient_id = patient.id,
        appointment_id = appointment.id,
        note = form.note.data
      )
      db.session.add(new_diagnosis)
      db.session.flush()
      diagnosis_details(new_diagnosis.id, diseases_ids)
    else:
      remove_diagnosis_disease(existing_diagnosis.id)
      diagnosis_details(existing_diagnosis.id, diseases_ids)
      form.populate_obj(existing_diagnosis)

    db.session.commit()
    flash("Diagnosis saved successfully", "success")
  except Exception as e:
    db.session.rollback()
    flash(f"Error: {str(e)}", "danger")

  return redirect(url_for("admin.appointment", appointment_id=appointment.unique_id))

def diagnosis_details(diagnosis_id, diagnosed_diseases_ids):
  diagnosis = Diagnosis.query.filter_by(id=diagnosis_id).first()
  for disease_id in diagnosed_diseases_ids:
    disease = Disease.query.filter_by(unique_id = disease_id).first()
    new_diagnosis_detail = DiagnosisDetails(
      diagnosis_id = diagnosis.id,
      disease_id = disease.id,
    )
    db.session.add(new_diagnosis_detail)
    db.session.commit()

def remove_diagnosis_disease(diagnosis_id):
  diagnosis = Diagnosis.query.filter_by(id=diagnosis_id).first()
  for diagnosis_detail in diagnosis.diagnosis_details:
    db.session.delete(diagnosis_detail)
    db.session.commit()

@admin.route("/prescribe/patient/<int:appointment_id>", methods=["POST"])
@login_required
@role_required(["Admin", "Lab Tech"])
def add_prescription(appointment_id):
  appointment = Appointment.query.filter_by(unique_id=appointment_id).first()
  if not appointment:
    flash("Appointment not found", "danger")
    return redirect(url_for("admin.home"))

  if appointment.is_active == False:
    flash("Appointment is not active", "warning")
    return redirect(url_for("admin.appointment", appointment_id=appointment.unique_id))

  form = PrescriptionForm()

  try:
    medicine_ids = request.form.getlist("medicines")
    patient = Patients.query.get(appointment.patient_id)
    existing_prescription = Prescription.query.filter_by(appointment_id=appointment.id, patient_id=patient.id, is_active=True).first()
    if not existing_prescription:
      new_prescription = Prescription(
        patient_id = patient.id,
        appointment_id = appointment.id,
        note = form.note.data
      )
      db.session.add(new_prescription)
      db.session.flush()
      prescription_details(new_prescription.id, medicine_ids)
      calculate_prescription_total(new_prescription.id)
    else:
      remove_prescribed_medicine(existing_prescription.id)
      prescription_details(existing_prescription.id, medicine_ids)
      calculate_prescription_total(existing_prescription.id)
      form.populate_obj(existing_prescription)

    db.session.commit()
  except Exception as e:
    db.session.rollback()
    flash(f"Error: {str(e)}", "danger")

  return redirect(url_for("admin.appointment", appointment_id=appointment.unique_id))

def prescription_details(prescription_id, prescribed_medicine_ids):
  prescription = Prescription.query.get(prescription_id)
  for medicine_id in prescribed_medicine_ids:
    medicine = Medicine.query.filter_by(unique_id=medicine_id).first()
    if medicine.quantity < 1:
      flash(f"Medicine {medicine.name} is out of stock", "info")
    else:
      new_prescription_detail = PrescriptionDetails(
        prescription_id = prescription.id,
        medicine_id = medicine.id,
        amount = medicine.price
      )
      db.session.add(new_prescription_detail)
      flash("Prescription saved successfully", "success")
      db.session.commit()

def calculate_prescription_total(prescription_id):
  prescription = Prescription.query.get(prescription_id)
  prescription_appointment = Appointment.query.get(prescription.appointment_id)
  prescription.total = sum([prescription_detail.amount for prescription_detail in prescription.prescription_details])
  prescription_appointment.total = sum([prescription_detail.amount for prescription_detail in prescription.prescription_details])
  db.session.commit()

def remove_prescribed_medicine(prescription_id):
  prescription = Prescription.query.filter_by(id=prescription_id).first()
  for prescription_detail in prescription.prescription_details:
    db.session.delete(prescription_detail)
    db.session.commit()

@admin.route("/complete/appointment/<int:appointment_id>")
@login_required
@role_required(["Admin", "Lab Tech"])
def complete_appointment(appointment_id):
  appointment = Appointment.query.filter_by(unique_id=appointment_id).first()
  if not appointment:
    flash("Appointment not found", "danger")
    return redirect(url_for("admin.home"))

  try:
    appointment_lab_analysis = LabAnalysis.query.filter_by(appointment_id=appointment.id, is_active=True).first()
    if appointment_lab_analysis:
      approve_lab_analysis.is_active = False
    appointment_diagnosis = Diagnosis.query.filter_by(appointment_id=appointment.id, is_active=True).first()
    if appointment_diagnosis:
      appointment_diagnosis.is_active = False
      appointment_diagnosis.date_closed = get_local_time()
    appointment_prescription = Prescription.query.filter_by(appointment_id=appointment.id, is_active=True).first()
    if appointment_prescription:
      appointment_prescription.is_active = False
      appointment_prescription.date_closed = get_local_time()
    appointment.is_active = False
    appointment.date_closed = get_local_time()
    db.session.commit()
    flash("Appointment completed successfully", "success")
  except Exception as e:
    db.session.rollback()
    flash(f"Error: {str(e)}", "danger")

  return redirect(url_for("admin.home"))

@admin.route("/pay/prescription/<int:prescription_id>")
@login_required
@role_required(["Admin", "Accountant"])
def prescription_payment(prescription_id):
  prescription = Prescription.query.filter_by(unique_id=prescription_id).first()
  if not prescription:
    flash("Prescription not found", "danger")
    return redirect(url_for("admin.home"))
  
  try:
    prescription_appointment = Appointment.query.get(prescription.appointment_id)
    if prescription_appointment:
      prescription_appointment.is_paid = True
      prescription_appointment.date_paid = get_local_time()
    prescription.is_paid = True
    prescription.date_paid = get_local_time()
    record_transaction(prescription.id)
    db.session.commit()
    flash("Prescription paid successfully", "success")

  except Exception as e:
    flash(f"Error: {str(e)}", "danger")
  
  return redirect(url_for("admin.home"))

def record_transaction(prescription_id):
  prescription = Prescription.query.get(prescription_id)
  prescription_details = PrescriptionDetails.query.filter_by(prescription_id=prescription.id).all()
  for prescription_detail in prescription_details:
    medicine = Medicine.query.filter_by(id=prescription_detail.medicine_id).first()
    if medicine:
      medicine.quantity = medicine.quantity - 1
  new_payment = Payment(
    amount = prescription.total,
    is_completed = True,
    date_paid = get_local_time(),
    prescription_id = prescription.id,
    patient_id = prescription.patient_id
  )
  db.session.add(new_payment)
  db.session.commit()

@admin.route("/export/transaction/<int:payment_id>")
def export_transaction(payment_id):
  payment = Payment.query.filter_by(unique_id=payment_id).first()
  if not payment:
    flash("Payment not found", "danger")
    return redirect(url_for("admin.home"))

  try:
    patient = Patients.query.get(payment.patient_id)
    generate_payment_pdf(patient.to_dict(), payment.to_dict())
    flash("Payment exported successfully", "success")
  except Exception as e:
    flash(f"{str(e)}", "danger")

  return redirect(url_for("admin.home"))

# @admin.route('/api/analytics')
# def get_analytics():
#   month = request.args.get('month', 'all')
#   year = request.args.get('year', get_local_time.year)
  
#   try:
#     # Get most diagnosed diseases
#     diseases_query = db.session.query(
#       Diagnosis.diagnosed_disease.name,
#       db.func.count(Diagnosis.id).label('count')
#     )
    
#     if month != 'all':
#       diseases_query = diseases_query.filter(
#         db.extract('month', Diagnosis.created_at) == month,
#         db.extract('year', Diagnosis.created_at) == year
#       )
    
#     top_diseases = diseases_query.group_by(Diagnosis.diagnosed_disease.name).order_by(db.desc('count')).limit(5).all()
    
#     # Get most prescribed medications
#     meds_query = db.session.query(
#       Prescription.prescribed_medicine.name,
#       db.func.count(Prescription.id).label('count')
#     )
    
#     if month != 'all':
#       meds_query = meds_query.filter(
#         db.extract('month', Prescription.created_at) == month,
#         db.extract('year', Prescription.created_at) == year
#       )
    
#     top_medications = meds_query.group_by(Prescription.prescribed_medicine.name).order_by(db.desc('count')).limit(5).all()
    
#     return jsonify({
#       'diseases': [{'name': d[0], 'count': d[1]} for d in top_diseases],
#       'medications': [{'name': m[0], 'count': m[1]} for m in top_medications]
#     })
      
#   except Exception as e:
#     return jsonify({'error': str(e)}), 500
