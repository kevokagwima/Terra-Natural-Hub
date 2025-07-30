from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_required, fresh_login_required
from Models.base_model import db, get_local_time
from Models.users import Role
from Models.users import Patients, PatientAddress, Staff
from Models.medicine import Medicine
from Models.diseases import Disease
from Models.payment import Payment
from Models.lab_analysis import LabAnalysis, LabAnalysisDetails
from Models.appointment import Appointment, Feedback
from Models.prescription import Prescription, PrescriptionDetails
from Models.diagnosis import Diagnosis, DiagnosisDetails
from Models.clinic import Clinic, ClinicType
from .form import AddPatientForm, DiagnosisForm, PrescriptionForm, LabAnalysisForm, AddDiseaseForm, AddMedicineForm, FeedbackForm, AddClinicForm, UpdatedPasswordForm
from Auth.form import StaffRegistrationForm
from Documents.export_pdf import generate_payment_pdf
from decorator import role_required
from collections import defaultdict
from sqlalchemy.sql import func, desc
from slugify import slugify

admin = Blueprint("admin", __name__)
region_districts = {
  "Arusha": ["Monduli", "Arusha", "Arumeru", "Karatu", "Longido", "Ngorongoro"],
  "Dar es Salaam": ["Ilala", "Kinondoni", "Temeke", "Kigamboni", "Ubungo"],
  "Dodoma": ["Bahi", "Chamwino", "Chemba", "Dodoma", "Kondoa", "Kongwa", "Mpwapwa"],
  "Geita": ["Bukombe", "Chato", "Geita", "Mbogwe", "Nyang'hwale"],
  "Iringa": ["Iringa", "Kilolo", "Mafinga Town", "Mufindi"],
  "Kagera": ["Biharamulo", "Bukoba", "Karagwe", "Kyerwa", "Missenyi", "Muleba", "Ngara"],
  "Katavi": ["Mlele", "Mpanda"],
  "Kigoma": ["Buhigwe", "Kakonko", "Kasulu", "Kibondo", "Kigoma", "Uvinz"],
  "Kilimanjaro": ["Hai", "Moshi", "Mwanga", "Rombo", "Same", "Siha"],
  "Lindi": ["Kilwa", "Lindi", "Liwale", "Nachingwea", "Ruangwa"],
  "Manyara": ["Babati", "Hanang", "Kiteto", "Mbulu", "Simanjiro"],
  "Mara": ["Bunda", "Butiama", "Musoma", "Rorya", "Serengeti", "Tarime"],
  "Mbeya": ["Busokelo", "Chunya", "Kyela", "Mbarali", "Mbeya", "Rungwe"],
  "Mororgoro": ["Gairo", "Kilombero", "Kilosa", "Morogoro", "Mvomero", "Ulanga"],
  "Mtwara": ["Masasi", "Mtwara", "Nanyumbu", "Newala", "Tandahimba"],
  "Mwanza": ["Ilemela", "Kwimba", "Magu", "Misungwi", "Nyamagana", "Sengerema", "Ukerewe"],
  "Njombe": ["Ludewa", "Makambako Town", "Makete", "Njombe", "Wanging'ombe"],
  "Pwani": ["Bagamoyo", "Kibaha", "Kisarawe", "Mafia", "Mkuranga", "Rufiji"],
  "Rukwa": ["Kalambo", "Nkasi", "Sumbawanga"],
  "Ruvuma": ["Mbinga", "Namtumbo", "Nyasa", "Songea", "Tunduru"],
  "Shinyanga": ["Kahama", "Kishapu", "Shinyanga"],
  "Simiyu": ["Bariadi", "Busega", "Itilima", "Maswa", "Meat"],
  "Singida": ["Ikungi", "Iramba", "Manyoni", "Mkalama", "Singida"],
  "Songwe": ["Ileje", "Mbozi", "Momba", "Songwe"],
  "Tabora": ["Igunga", "Kaliua", "Nzega", "Sikonge", "Tabora", "Uyu"],
  "Tanga": ["Handeni", "Kilindi", "Korogwe", "Lushoto", "Mkinga", "Muheza", "Pangani", "Tanga"],
  "Zanzibar": ["Zanzibar Central/South", "Zanzibar North", "Zanzibar Urban/West"]
}

@admin.route("/")
@admin.route("/home")
@admin.route("/branch/select", methods=["POST", "GET"])
@login_required
@fresh_login_required
def select_branch():
  form = AddClinicForm()

  if form.validate_on_submit():
    try:
      new_clinic = Clinic(
        name = form.name.data,
        alias = slugify(form.name.data),
        region = form.region.data,
        district = form.district.data,
        clinic_type_id = ClinicType.query.filter_by(name=form.branch_type.data).first().id
      )
      db.session.add(new_clinic)
      db.session.commit()
      flash("Branch added successfully", "success")
      return redirect(url_for("admin.select_branch"))
    except Exception as e:
      flash(f"{str(e)}", "danger")
      return redirect(url_for("admin.select_branch"))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", "danger")
      return redirect(request.referrer)
  
  context = {
    "form": form,
    "clinics": Clinic.query.all()
  }

  return render_template("Main/select-branch.html", **context)

@admin.route("/load/branch/<string:branch_name>")
def load_clinic(branch_name):
  clinic = Clinic.query.filter_by(alias=branch_name).first()
  if not clinic:
    flash("Branch not found", "danger")
    return redirect(url_for('admin.select_branch'))
  session["clinic_id"] = clinic.id
  return redirect(url_for('admin.dashboard'))

@admin.route("/dashboard")
@login_required
@fresh_login_required
def dashboard():
  if not "clinic_id" in session:
    flash("Select a clinic", "warning")
    return redirect(url_for('admin.select_branch'))
  
  form = StaffRegistrationForm()
  form.branch.choices = [(clinic.unique_id, clinic.name) for clinic in Clinic.query.all()]
  form.role.choices = [(role.unique_id, role.name) for role in Role.query.all()]
  
  diagnosis_disease_ids = [diagnosis for diagnosis in db.session.query(DiagnosisDetails.disease_id, func.count(DiagnosisDetails.disease_id).label('count')).group_by(DiagnosisDetails.disease_id).order_by(func.count(DiagnosisDetails.disease_id).desc()).limit(limit=5).all()]

  prescription_medicine_ids = [prescription for prescription in db.session.query(PrescriptionDetails.medicine_id, func.count(PrescriptionDetails.medicine_id).label('count')).group_by(PrescriptionDetails.medicine_id).order_by(func.count(PrescriptionDetails.medicine_id).desc()).limit(limit=5).all()]

  context = {
    "patients": Patients.query.filter_by(clinic_id=session["clinic_id"]).all(),
    "staffs": Staff.query.all(),
    "payments" : Payment.query.filter_by(clinic_id=session["clinic_id"]).all(),
    "medicines" : Medicine.query.all(),
    "diseases" : Disease.query.all(),
    "all_diagnosis" : Diagnosis.query.filter_by(clinic_id=session["clinic_id"]).all(),
    "prescriptions" : Prescription.query.filter_by(clinic_id=session["clinic_id"]).all(),
    "appointments" : Appointment.query.filter_by(clinic_id=session["clinic_id"]).all(),
    "lab_tests" : LabAnalysis.query.filter_by(clinic_id=session["clinic_id"]).all(),
    "diagnosis_disease_ids": diagnosis_disease_ids,
    "prescription_medicine_ids": prescription_medicine_ids,
    "clinic": Clinic.query.get(session["clinic_id"]),
    "form": form,
    "update_password_form": UpdatedPasswordForm()
  }
  
  return render_template("Main/home.html", **context)

@admin.route("/find-patient/<string:search_text>")
@login_required
@fresh_login_required
def patient_search(search_text):
  patients = Patients.query.filter(Patients.first_name.like("%" + search_text.capitalize() + "%"), Patients.clinic_id == session["clinic_id"]).all()
  patients_count = Patients.query.filter(Patients.first_name.like("%" + search_text.capitalize() + "%"), Patients.clinic_id == session["clinic_id"]).count()

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

@admin.route("/add/medicine", methods=["POST", "GET"])
@login_required
@fresh_login_required
@role_required(["Admin"])
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
      return redirect(url_for('admin.dashboard'))
        
    except Exception as e:
      db.session.rollback()
      flash('Error adding medicine: ' + str(e), 'danger')
      return redirect(url_for('admin.add_medicine'))
  
  context = {
    "form": form,
    "clinic": Clinic.query.get(session["clinic_id"])
  }

  return render_template("Main/add-medicine.html", **context)

@admin.route("/edit/medicine/<int:medicine_id>", methods=["POST", "GET"])
@login_required
@fresh_login_required
@role_required(["Admin", "Stock Controller"])
def edit_medicine(medicine_id):
  medicine = Medicine.query.filter_by(unique_id=medicine_id).first()
  if not medicine:
    flash("Medicine not found", category="danger")
    return redirect(url_for("admin.dashboard"))
  
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
    "title_message": "Edit",
    "clinic": Clinic.query.get(session["clinic_id"])
  }

  return render_template("Main/add-medicine.html", **context)

@admin.route("/remove/medicine/<int:medicine_id>")
@login_required
@fresh_login_required
@role_required(["Admin"])
def remove_medicine(medicine_id):
  medicine = Medicine.query.filter_by(unique_id=medicine_id).first()
  if not medicine:
    flash("Medicine not found", category="danger")
    return redirect(url_for("admin.dashboard"))
  
  try:
    db.session.delete(medicine)
    db.session.commit()
    flash("Medicine removed successfully", "success")
  except Exception as e:
    flash(f"Error: {str(e)}", "danger")

  return redirect(url_for('admin.dashboard'))

@admin.route("/add/disease", methods=["POST", "GET"])
@login_required
@fresh_login_required
@role_required(["Admin"])
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
      return redirect(url_for('admin.dashboard'))
        
    except Exception as e:
      db.session.rollback()
      flash('Error adding medicine: ' + str(e), 'danger')
      return redirect(url_for('admin.add_disease'))
  
  context = {
    "form": form,
    "clinic": Clinic.query.get(session["clinic_id"])
  }

  return render_template("Main/add-disease.html", **context)

@admin.route("/edit/disease/<int:disease_id>", methods=["POST", "GET"])
@login_required
@fresh_login_required
@role_required(["Admin"])
def edit_disease(disease_id):
  disease = Disease.query.filter_by(unique_id=disease_id).first()
  if not disease:
    flash("Disease not found", category="danger")
    return redirect(url_for("admin.dashboard"))
  
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
    "title_message": "Edit",
    "clinic": Clinic.query.get(session["clinic_id"])
  }

  return render_template("Main/add-disease.html", **context)

@admin.route("/remove/disease/<int:disease_id>")
@login_required
@fresh_login_required
@role_required(["Admin"])
def remove_disease(disease_id):
  disease = Disease.query.filter_by(unique_id=disease_id).first()
  if not disease:
    flash("Disease not found", category="danger")
    return redirect(url_for("admin.dashboard"))
  
  try:
    db.session.delete(disease)
    db.session.commit()
    flash("Disease removed successfully", "success")
  except Exception as e:
    flash(f"Error: {str(e)}", "danger")

  return redirect(url_for('admin.dashboard'))

@admin.route("/add/patient", methods=["POST", "GET"])
@login_required
@fresh_login_required
@role_required(["Admin", "Clerk"])
def add_patient():
  form = AddPatientForm()
  form.district.choices = [('', 'Select District')]
  if 'region' in request.form:
    region = request.form['region']
    form.district.choices = [(d, d) for d in region_districts.get(region, [])]
  if form.validate_on_submit():
    try:
      new_patient = Patients(
        first_name = form.first_name.data,
        last_name = form.last_name.data,
        age = form.age.data,
        gender = form.gender.data,
        phone_number_1 = form.phone_number_1.data,
        phone_number_2 = form.phone_number_2.data,
        branch = form.branch.data,
        clinic_id = session["clinic_id"]
      )
      db.session.add(new_patient)
      db.session.commit()
      if form.region.data or form.district.data or form.location.data:
        new_patient_address = PatientAddress(
          region = form.region.data,
          district = form.district.data,
          location = form.location.data
        )
        db.session.add(new_patient_address)
      db.session.commit()
      new_patient.address_id = new_patient_address.id
      db.session.commit()
      flash('Patient created successfully!', 'success')
      return redirect(url_for('admin.patient_profile', patient_id=new_patient.unique_id))
        
    except Exception as e:
      db.session.rollback()
      flash('Error creating patient: ' + str(e), 'danger')
      return redirect(url_for('admin.add_patient'))
  
  context = {
    "form": form,
    "clinic": Clinic.query.get(session["clinic_id"])
  }

  return render_template("Main/add-patient.html", **context)

@admin.route("/get-districts/<region>")
@login_required
@fresh_login_required
@role_required(["Admin", "Clerk"])
def get_districts(region):
  return jsonify(districts=region_districts.get(region, []))

@admin.route("/edit/patient/<int:patient_id>", methods=["POST", "GET"])
@login_required
@fresh_login_required
@role_required(["Admin", "Clerk"])
def edit_patient(patient_id):
  patient = Patients.query.filter_by(unique_id = patient_id).first()
  if not patient:
    flash("Patient not found", "danger")
    return redirect(url_for("admin.dashboard"))

  patient_address = PatientAddress.query.filter_by(id=patient.address_id).first()
  form = AddPatientForm(obj=patient)
  form.district.choices = [('', 'Select District')]
  if "region" in request.form:
    region = request.form['region']
    form.district.choices = [(d, d) for d in region_districts.get(region, [])]
      
  if form.validate_on_submit():
    try:
      form.populate_obj(patient)
      if not patient_address:
        new_patient_address = PatientAddress(
          region = form.region.data,
          district = form.district.data,
          location = form.location.data,
        )
        db.session.add(new_patient_address)
        db.session.commit()
        patient.address_id = new_patient_address.id
      else:
        if form.region.data or form.district.data or form.location.data:
          patient_address.region = form.region.data
          patient_address.district = form.district.data
          patient_address.location = form.location.data
      db.session.commit()
      flash("Patient details updated successfully", "success")
    except Exception as e:
      flash(f"Error submitting form: {str(e)}", "danger")

    return redirect(url_for("admin.edit_patient", patient_id=patient.unique_id))

  context = {
    "patient": patient,
    "form": form,
    "title_message": "Edit",
    "clinic": Clinic.query.get(session["clinic_id"])
  }

  return render_template("Main/add-patient.html", **context)

@admin.route("/remove-patient/<int:patient_id>")
@login_required
@fresh_login_required
@role_required(["Admin"])
def remove_patient(patient_id):
  patient = Patients.query.filter_by(unique_id = patient_id).first()
  if not patient:
    flash("Patient not found", "danger")
    return redirect(url_for("admin.dashboard"))
  db.session.delete(patient)
  db.session.commit()
  flash("Patient removed successfully", "success")
  return redirect(url_for('admin.dashboard'))

@admin.route("/remove-staff/<int:staff_id>")
@login_required
@fresh_login_required
@role_required(["Admin"])
def remove_staff(staff_id):
  staff = Staff.query.filter_by(unique_id = staff_id).first()
  if not staff:
    flash("Staff not found", "danger")
  else:
    db.session.delete(staff)
    db.session.commit()
    flash("Staff removed successfully", "success")
  return redirect(url_for('admin.dashboard'))

@admin.route("/profile/patient/<int:patient_id>")
@login_required
@fresh_login_required
@role_required(["Admin", "Clerk"])
def patient_profile(patient_id):
  patient = Patients.query.filter_by(unique_id = patient_id).first()
  if not patient:
    flash("Patient not found", "danger")
    return redirect(url_for("admin.dashboard"))

  patient_address = PatientAddress.query.filter_by(id=patient.address_id).first()
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
    "clinic": Clinic.query.get(session["clinic_id"])
  }

  return render_template('Main/patient-profile.html', **context)

@admin.route("/create-appointment/<int:patient_id>")
@login_required
@fresh_login_required
@role_required(["Admin", "Lab Tech", "Clerk"])
def create_appointment(patient_id):
  patient = Patients.query.filter_by(unique_id=patient_id).first()
  if not patient:
    flash("Failed to create appointment, patient not found", "danger")
    return redirect(url_for("admin.dashboard"))
  
  existing_appointment = Appointment.query.filter_by(patient_id=patient.id, is_active=True).first()

  if not existing_appointment:
    new_appointment = Appointment(
      patient_id = patient.id,
      clinic_id = session["clinic_id"]
    )
    db.session.add(new_appointment)
    db.session.commit()
    return redirect(url_for("admin.appointment", appointment_id=new_appointment.unique_id))

  return redirect(url_for("admin.appointment", appointment_id=existing_appointment.unique_id))

@admin.route("/appointment/<int:appointment_id>")
@login_required
@fresh_login_required
@role_required(["Admin", "Lab Tech", "Clerk"])
def appointment(appointment_id):
  appointment = Appointment.query.filter_by(unique_id=appointment_id).first()
  if not appointment:
    flash("Appointment not found", "danger")
    return redirect(url_for("admin.dashboard"))
  
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
    "feedback": Feedback.query.filter_by(appointment_id=appointment.id).first(),
    "form": FeedbackForm(),
    "clinic": Clinic.query.get(session["clinic_id"])
  }

  return render_template("Main/appointment.html", **context)

@admin.route("/lab-analysis/<int:appointment_id>", methods=["POST"])
@login_required
@fresh_login_required
@role_required(["Admin", "Clerk"])
def add_lab_analysis(appointment_id):
  appointment = Appointment.query.filter_by(unique_id=appointment_id).first()
  if not appointment:
    flash("Appointment not found", "danger")
    return redirect(url_for("admin.dashboard"))

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
        clinic_id = session["clinic_id"]
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
@fresh_login_required
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
@fresh_login_required
@role_required(["Admin", "Lab Tech"])
def approve_lab_analysis(lab_analysis_id):
  lab_analysis = LabAnalysis.query.filter_by(unique_id=lab_analysis_id).first()
  if not lab_analysis:
    flash("Lab analysis not found", "danger")
    return redirect(url_for("admin.dashboard"))
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
@fresh_login_required
@role_required(["Admin", "Lab Tech"])
def add_diagnosis(appointment_id):
  appointment = Appointment.query.filter_by(unique_id=appointment_id).first()
  if not appointment:
    flash("Appointment not found", "danger")
    return redirect(url_for("admin.dashboard"))
  
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
        note = form.note.data,
        clinic_id = session["clinic_id"]
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
      clinic_id = session["clinic_id"]
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
@fresh_login_required
@role_required(["Admin", "Lab Tech"])
def add_prescription(appointment_id):
  appointment = Appointment.query.filter_by(unique_id=appointment_id).first()
  if not appointment:
    flash("Appointment not found", "danger")
    return redirect(url_for("admin.dashboard"))

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
        note = form.note.data,
        clinic_id = session["clinic_id"]
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
        amount = medicine.price,
        clinic_id = session["clinic_id"]
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
@fresh_login_required
@role_required(["Admin", "Lab Tech"])
def complete_appointment(appointment_id):
  appointment = Appointment.query.filter_by(unique_id=appointment_id).first()
  if not appointment:
    flash("Appointment not found", "danger")
    return redirect(url_for("admin.dashboard"))

  try:
    if not appointment.lab_analysis and not appointment.diagnosis and not appointment.prescription:
      flash("Appointment missing either an approved lab test or diagnosis or prescription", "warning")
      return redirect(request.referrer)
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

  return redirect(url_for("admin.dashboard"))

@admin.route("/patient/feedback/<int:appointment_id>", methods=["POST"])
@login_required
@fresh_login_required
@role_required(["Admin"])
def patient_feedback(appointment_id):
  try:
    appointment = Appointment.query.filter_by(unique_id=appointment_id).first()
    if not appointment:
      flash("Appointment not found", "danger")
      return redirect(url_for("admin.dashboard"))
    
    form = FeedbackForm()
    if form.validate_on_submit():
      new_feeback = Feedback(
        status = form.feedback.data,
        appointment_id = appointment.id
      )
      db.session.add(new_feeback)
      db.session.commit()
      flash("Feedback recorded successfully", "success")
      return redirect(url_for("admin.appointment", appointment_id=appointment.unique_id))
    
  except Exception as e:
    flash(f"{str(e)}", "danger")
    return redirect(request.referrer)

@admin.route("/pay/prescription/<int:prescription_id>")
@login_required
@fresh_login_required
@role_required(["Admin", "Accountant"])
def prescription_payment(prescription_id):
  prescription = Prescription.query.filter_by(unique_id=prescription_id).first()
  if not prescription:
    flash("Prescription not found", "danger")
    return redirect(url_for("admin.dashboard"))
  
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
  
  return redirect(url_for("admin.dashboard"))

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
    patient_id = prescription.patient_id,
    clinic_id = session["clinic_id"]
  )
  db.session.add(new_payment)
  db.session.commit()

@admin.route("/export/transaction/<int:payment_id>")
@login_required
@fresh_login_required
def export_transaction(payment_id):
  payment = Payment.query.filter_by(unique_id=payment_id).first()
  if not payment:
    flash("Payment not found", "danger")
    return redirect(url_for("admin.dashboard"))

  try:
    patient = Patients.query.get(payment.patient_id)
    return generate_payment_pdf(patient.to_dict(), payment.to_dict())
  except Exception as e:
    flash(f"{str(e)}", "danger")

  return redirect(url_for("admin.dashboard"))

@admin.route("/analytics", methods=["POST", "GET"])
@login_required
@fresh_login_required
def analytics():
  details = db.session.query(
    DiagnosisDetails.id,
    DiagnosisDetails.diagnosis_id,
    DiagnosisDetails.disease_id
  ).filter(DiagnosisDetails.clinic_id == session["clinic_id"]).all()
  prescription_details = db.session.query(
    PrescriptionDetails.id,
    PrescriptionDetails.prescription_id,
    PrescriptionDetails.medicine_id
  ).filter(PrescriptionDetails.clinic_id == session["clinic_id"]).all()

  month_selected = 0
  region_selected = ""

  if request.method == "POST":
    region_selected = request.form.get("region-filter")
    month_selected = request.form.get("month-filter")

    if not region_selected and not month_selected:
      flash("Select at least one filter from the dropdown before submitting", "warning")
      return redirect(url_for("admin.analytics"))

    if not month_selected:
      month_selected = 0

    if region_selected:
      details = db.session.query(
        DiagnosisDetails.id,
        DiagnosisDetails.diagnosis_id,
        DiagnosisDetails.disease_id,
        Disease.name,
        func.count(DiagnosisDetails.disease_id).label('count')
        ).join(
            DiagnosisDetails,
            DiagnosisDetails.disease_id == Disease.id
        ).join(
            Diagnosis,
            Diagnosis.id == DiagnosisDetails.diagnosis_id
        ).join(
            Appointment,
            Appointment.id == Diagnosis.appointment_id
        ).join(
            Patients,
            Patients.id == Appointment.patient_id
        ).join(
            PatientAddress,
            PatientAddress.id == Patients.address_id
        ).filter(
            PatientAddress.region == region_selected, DiagnosisDetails.clinic_id == session["clinic_id"]
        ).group_by(
            DiagnosisDetails.id,
            DiagnosisDetails.disease_id,
            DiagnosisDetails.diagnosis_id,
            Disease.name,
        ).order_by(
            desc('count')
        ).all()

      prescription_details = db.session.query(
        PrescriptionDetails.id,
        PrescriptionDetails.prescription_id,
        PrescriptionDetails.medicine_id,
        Medicine.name,
        func.count(PrescriptionDetails.medicine_id).label('count')
        ).join(
            PrescriptionDetails,
            PrescriptionDetails.medicine_id == Medicine.id
        ).join(
            Prescription,
            Prescription.id == PrescriptionDetails.prescription_id
        ).join(
            Appointment,
            Appointment.id == Prescription.appointment_id
        ).join(
            Patients,
            Patients.id == Appointment.patient_id
        ).join(
            PatientAddress,
            PatientAddress.id == Patients.address_id
        ).filter(
            PatientAddress.region == region_selected, PrescriptionDetails.clinic_id == session["clinic_id"]
        ).group_by(
            PrescriptionDetails.id,
            PrescriptionDetails.medicine_id,
            PrescriptionDetails.prescription_id,
            Medicine.name,
        ).order_by(
            desc('count')
        ).all()

    if region_selected and month_selected and month_selected != 0:
      details = db.session.query(
        DiagnosisDetails.id,
        DiagnosisDetails.diagnosis_id,
        DiagnosisDetails.disease_id,
        Disease.name,
        func.count(DiagnosisDetails.disease_id).label('count')
        ).join(
            DiagnosisDetails,
            DiagnosisDetails.disease_id == Disease.id
        ).join(
            Diagnosis,
            Diagnosis.id == DiagnosisDetails.diagnosis_id
        ).join(
            Appointment,
            Appointment.id == Diagnosis.appointment_id
        ).join(
            Patients,
            Patients.id == Appointment.patient_id
        ).join(
            PatientAddress,
            PatientAddress.id == Patients.address_id
        ).filter(
            PatientAddress.region == region_selected, DiagnosisDetails.month_created == month_selected, DiagnosisDetails.clinic_id == session["clinic_id"]
        ).group_by(
            DiagnosisDetails.id,
            DiagnosisDetails.disease_id,
            DiagnosisDetails.diagnosis_id,
            Disease.name,
        ).order_by(
            desc('count')
        ).all()
      prescription_details = db.session.query(
        PrescriptionDetails.id,
        PrescriptionDetails.prescription_id,
        PrescriptionDetails.medicine_id,
        Medicine.name,
        func.count(PrescriptionDetails.medicine_id).label('count')
        ).join(
            PrescriptionDetails,
            PrescriptionDetails.medicine_id == Medicine.id
        ).join(
            Prescription,
            Prescription.id == PrescriptionDetails.prescription_id
        ).join(
            Appointment,
            Appointment.id == Prescription.appointment_id
        ).join(
            Patients,
            Patients.id == Appointment.patient_id
        ).join(
            PatientAddress,
            PatientAddress.id == Patients.address_id
        ).filter(
            PatientAddress.region == region_selected, PrescriptionDetails.month_created == month_selected, PrescriptionDetails.clinic_id == session["clinic_id"]
        ).group_by(
            PrescriptionDetails.id,
            PrescriptionDetails.medicine_id,
            PrescriptionDetails.prescription_id,
            Medicine.name,
        ).order_by(
            desc('count')
        ).all()

    if month_selected and month_selected != 0 and not region_selected:
      details = db.session.query(
        DiagnosisDetails.id,
        DiagnosisDetails.diagnosis_id,
        DiagnosisDetails.disease_id
      ).filter(DiagnosisDetails.month_created == int(month_selected), Diagnosis.clinic_id == session["clinic_id"]).all()
      prescription_details = db.session.query(
        PrescriptionDetails.id,
        PrescriptionDetails.prescription_id,
        PrescriptionDetails.medicine_id
      ).filter(PrescriptionDetails.month_created == int(month_selected), PrescriptionDetails.clinic_id == session["clinic_id"]).all()

  # Then process in Python to count and group
  disease_counts = defaultdict(list)

  for detail in details:
    disease_counts[detail.disease_id].append({
      'diagnosis_detail_id': detail.id,
      'diagnosis_id': detail.diagnosis_id
    })

  # Convert to final structure
  result = []
  for disease_id, entries in disease_counts.items():
    result.append({
      'disease_id': disease_id,
      'count': len(entries),
      'diagnoses': entries
    })

  medicine_counts = defaultdict(list)

  for detail in prescription_details:
    medicine_counts[detail.medicine_id].append({
      'prescription_detail_id': detail.id,
      'prescription_id': detail.prescription_id
    })

  # Convert to final structure
  prescription_result = []
  for medicine_id, entries in medicine_counts.items():
    prescription_result.append({
      'medicine_id': medicine_id,
      'count': len(entries),
      'prescriptions': entries
    })

  # Sort by count descending
  result.sort(key=lambda x: x['count'], reverse=True)
  prescription_result.sort(key=lambda x: x['count'], reverse=True)

  context = {
    "results": result,
    "prescription_results": prescription_result,
    "diseases": Disease.query.all(),
    "medicines": Medicine.query.all(),
    "all_diagnosis": Diagnosis.query.all(),
    "prescriptions": Prescription.query.all(),
    "diagnosis_details": DiagnosisDetails.query.all(),
    "patients": Patients.query.all(),
    "month_selected": int(month_selected),
    "regions": ["Arusha","Dar es Salaam","Dodoma","Geita","Iringa","Kagera","Katavi","Kigoma","Kilimanjaro","Lindi","Manyara","Mara","Mbeya","Mororgoro","Mtwara","Mwanza","Njombe","Pwani","Rukwa","Ruvuma","Shinyanga","Simiyu","Singida","Songwe","Tabora","Tanga","Zanzibar"
    ],
    "region_selected": region_selected,
    "clinic": Clinic.query.get(session["clinic_id"])
  }

  return render_template("Main/analytics.html", **context)
