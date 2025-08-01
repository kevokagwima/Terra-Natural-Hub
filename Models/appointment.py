from Models.base_model import db, BaseModel, get_local_time
from Models.diagnosis import Diagnosis
from Models.prescription import Prescription
from Models.lab_analysis import LabAnalysis

class Appointment(BaseModel, db.Model):
  __tablename__ = "appointment"
  patient_id = db.Column(db.Integer(), db.ForeignKey("patient.id"))
  clinic_id = db.Column(db.Integer(), db.ForeignKey("clinic.id"))
  is_active = db.Column(db.Boolean(), default=True)
  is_paid = db.Column(db.Boolean(), default=False)
  date_created = db.Column(db.DateTime(), default=get_local_time())
  date_closed = db.Column(db.DateTime())
  date_paid = db.Column(db.DateTime())
  total = db.Column(db.Integer(), default=0)
  diagnosis = db.relationship("Diagnosis", backref="appointment_diagnosis", lazy=True)
  prescription = db.relationship("Prescription", backref="appointment_prescription", lazy=True)
  lab_analysis = db.relationship("LabAnalysis", backref="appointment_lab_analysis", lazy=True)
  feedback = db.relationship("Feedback", backref="appointment_feedback", lazy=True)

  def __repr__(self):
    return f"{self.patient_id}"

class Feedback(BaseModel, db.Model):
  __tablename__ = "feedback"
  appointment_id = db.Column(db.Integer(), db.ForeignKey("appointment.id"))
  status = db.Column(db.String(20), nullable=False)
  date_recorded = db.Column(db.DateTime(), default=get_local_time())
