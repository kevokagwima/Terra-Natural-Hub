from Models.base_model import db, BaseModel, get_local_time
from Models.appointment import Appointment
from Models.diagnosis import Diagnosis
from Models.prescription import Prescription
from Models.payment import Payment
from Models.lab_analysis import LabAnalysis
from Models.notification import Notification

class ClinicType(BaseModel, db.Model):
  __tablename__ = "clinic_type"
  name = db.Column(db.String(100), nullable=False)
  clinic = db.relationship("Clinic", backref="clinic_type", lazy=True)

  def __str__(self):
    return self.name

class Clinic(BaseModel, db.Model):
  __tablename__ = "clinic"
  name = db.Column(db.String(100), nullable=False)
  alias = db.Column(db.String(100), nullable=False)
  region = db.Column(db.String(50), nullable=False)
  district = db.Column(db.String(50), nullable=False)
  is_active = db.Column(db.Boolean(), default=True)
  date_created = db.Column(db.DateTime(), default=get_local_time())
  clinic_type_id = db.Column(db.Integer(), db.ForeignKey("clinic_type.id"))
  appointment = db.relationship("Appointment", backref="clinic_appointment", lazy=True)
  diagnosis = db.relationship("DiagnosisDetails", backref="clinic_diagnosis", lazy=True)
  prescription = db.relationship("PrescriptionDetails", backref="clinic_prescription", lazy=True)
  payment = db.relationship("Payment", backref="clinic_payment", lazy=True)
  patients = db.relationship("Patients", backref="clinic_patients", lazy=True)
  staff = db.relationship("Staff", backref="clinic_staff", lazy=True)
  lab_analysis = db.relationship("LabAnalysis", backref="clinic_labanalysis", lazy=True)
  inventory = db.relationship("Inventory", backref="clinic_inventory", lazy=True)
  notification = db.relationship("Notification", backref="clinic_notifications", lazy=True)

  def __repr__(self):
    return f"{self.name}"
