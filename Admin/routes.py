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
  diagnosed_disease_ids = []

  # if diagnosis:
  #   for diagnosis in diagnosis:
  #     diagnosed_disease_ids.append(diagnosis.disease_id)
  #   diagnosis = Counter(diagnosed_disease_ids)
  #   most_diagnosed_diseases, diagnosed_count = diagnosis.most_common(1)[0]

  #   #Most prescribed medication
  #   prescription_data = Prescription.query.all()
  #   prescribed_medicine_ids = []
  #   for prescription in prescription_data:
  #     prescribed_medicine_ids.append(prescription.medicine_id)
  #   prescriptions = Counter(prescribed_medicine_ids)
  #   most_prescribed_medicine, prescribed_count = prescriptions.most_common(1)[0]
    
  #   #Paste below here
  #   result = (
  #     db.session.query(
  #         PatientAddress.region,
  #         func.string_agg(cast(Diagnosis.disease_id, String(10)), literal_column("','")).label("disease_ids")
  #     )
  #     .join(Patients, Patients.location == PatientAddress.id)
  #     .join(Diagnosis, Diagnosis.client_id == Patients.id)
  #     .group_by(PatientAddress.region)
  #     .all()
  #   )
  #   output = {row.region: [int(d) for d in row.disease_ids.split(",")] if row.disease_ids else [] for row in result}
  #   regions_with_data = list(output.keys())
  #   values = list(output.values())

  #   # Load Tanzania GeoJSON data
  #   with open("tanzania.geojson", "r", encoding="utf-8") as f:
  #     tanzania_geo = json.load(f)
    
  #   data = {
  #     "Region": regions_with_data,
  #     "Disease": values
  #   }
  #   state_data = pd.DataFrame(data)

  #   # Create a map centered on Tanzania
  #   m = folium.Map(location=[-6.369028, 34.888822], zoom_start=6)

  #   folium.GeoJson(
  #         tanzania_geo,
  #         name="Region Borders",
  #         style_function=lambda feature: {
  #             "fillColor": "yellow",  # Keep regions yellow
  #             "color": "black",  # Border color
  #             "weight": 2,  # Border thickness
  #         },
  #         tooltip=folium.GeoJsonTooltip(
  #             fields=["shapeName"],  # Adjust based on your GeoJSON properties
  #             aliases=["Region:"],
  #             sticky=True
  #         )
  #     ).add_to(m)


  #   for feature in tanzania_geo["features"]:
  #     region_name = feature["properties"]["shapeName"]
  #     feature["properties"]["DiseaseCount"] = len(output.get(region_name, []))
  #     diagnosed_diseases = output.get(region_name, [])
  #     most_diagnosed_disease = Counter(diagnosed_diseases).most_common(1)
  #     if most_diagnosed_disease:
  #       x,y = most_diagnosed_disease[0]
  #       most_diagnosed_disease_name= [disease.name for disease in diseases if disease.id == x]
  #       feature["properties"]["MostDiagnosed"] = [most_diagnosed_disease_name[0]] if most_diagnosed_disease_name else ["none"]
  #     else:
  #       feature["properties"]["MostDiagnosed"] = ["none"]

  #     feature["properties"]["DiseaseNames"] = [disease.name for disease in diseases for disease_id in output.get(region_name, []) if disease.id == disease_id]

  #   # Add a hover tooltip to display region name & disease count
  #   folium.GeoJson(
  #       tanzania_geo,
  #       style_function=lambda feature: {
  #           "fillColor": "transparent", 
  #           "color": "transparent"
  #       },
  #       tooltip=folium.GeoJsonTooltip(
  #           fields=["shapeName","DiseaseCount","DiseaseNames","MostDiagnosed"],
  #           aliases=["Region:","Disease count:","Disease name:","Most diagnosed:"],
  #           labels=True,
  #           sticky=False
  #       )
  #       # Manually add disease count data to each region in GeoJSON

  #     ).add_to(m)

  #   # Add layer control
  #   folium.LayerControl().add_to(m)

  #   # Store map HTML in a variable
  #   map_html = m.get_root().render()
  #   with open("templates/tanzania_map.html", "w", encoding="utf-8") as f:
  #     f.write(map_html)
  #   return render_template("home.html",Patients=Patients, medicines=medicines, diseases=diseases ,client_medicines=client_medicines,payments=payments, prescriptions=prescriptions, most_prescribed_medicine=most_prescribed_medicine, prescribed_count=prescribed_count, most_diagnosed_diseases=most_diagnosed_diseases, diagnosed_count=diagnosed_count)
  # else:
  
  context = {
    "patients": patients,
    "client_medicines" : client_medicines, 
    "payments" : payments,
    "medicines" : medicines,
    "diseases" : diseases,
    "all_diagnosis" : diagnosis,
    "prescriptions" : prescriptions,
    "appointments" : appointments,
  }
  
  return render_template("Main/home.html", **context)

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
      form.populate_obj(medicine)
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

  lab_analysis = LabAnalysis.query.filter_by(appointment_id=appointment.id).first()
  if lab_analysis:
    lab_analysis_details = LabAnalysisDetails.query.filter_by(lab_analysis_id=lab_analysis.id).all()
  else:
    lab_analysis_details = []

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
    "lab_analysis_details": lab_analysis_details,
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
    existing_lab_analysis = LabAnalysis.query.filter_by(appointment_id=appointment.id).first()
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
    flash("Prescription saved successfully", "success")
  except Exception as e:
    db.session.rollback()
    flash(f"Error: {str(e)}", "danger")

  return redirect(url_for("admin.appointment", appointment_id=appointment.unique_id))

def prescription_details(prescription_id, prescribed_medicine_ids):
  prescription = Prescription.query.get(prescription_id)
  for medicine_id in prescribed_medicine_ids:
    medicine = Medicine.query.filter_by(unique_id=medicine_id).first()
    new_prescription_detail = PrescriptionDetails(
      prescription_id = prescription.id,
      medicine_id = medicine.id,
      amount = medicine.price
    )
    db.session.add(new_prescription_detail)
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

@admin.route('/api/analytics')
def get_analytics():
  month = request.args.get('month', 'all')
  year = request.args.get('year', get_local_time.year)
  
  try:
    # Get most diagnosed diseases
    diseases_query = db.session.query(
      Diagnosis.diagnosed_disease.name,
      db.func.count(Diagnosis.id).label('count')
    )
    
    if month != 'all':
      diseases_query = diseases_query.filter(
        db.extract('month', Diagnosis.created_at) == month,
        db.extract('year', Diagnosis.created_at) == year
      )
    
    top_diseases = diseases_query.group_by(Diagnosis.diagnosed_disease.name).order_by(db.desc('count')).limit(5).all()
    
    # Get most prescribed medications
    meds_query = db.session.query(
      Prescription.prescribed_medicine.name,
      db.func.count(Prescription.id).label('count')
    )
    
    if month != 'all':
      meds_query = meds_query.filter(
        db.extract('month', Prescription.created_at) == month,
        db.extract('year', Prescription.created_at) == year
      )
    
    top_medications = meds_query.group_by(Prescription.prescribed_medicine.name).order_by(db.desc('count')).limit(5).all()
    
    return jsonify({
      'diseases': [{'name': d[0], 'count': d[1]} for d in top_diseases],
      'medications': [{'name': m[0], 'count': m[1]} for m in top_medications]
    })
      
  except Exception as e:
    return jsonify({'error': str(e)}), 500
