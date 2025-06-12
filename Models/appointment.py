from Models.base_model import db, BaseModel, get_local_time
from Models.diagnosis import Diagnosis
from Models.prescription import Prescription
from Models.lab_analysis import LabAnalysis

class Appointment(BaseModel, db.Model):
  __tablename__ = "appointment"
  patient_id = db.Column(db.Integer(), db.ForeignKey("patient.id"))
  is_active = db.Column(db.Boolean(), default=True)
  date_created = db.Column(db.DateTime(), default=get_local_time())
  date_closed = db.Column(db.DateTime())
  diagnosis = db.relationship("Diagnosis", backref="appointment_diagnosis", lazy=True)
  prescription = db.relationship("Prescription", backref="appointment_prescription", lazy=True)
  lab_analysis = db.relationship("LabAnalysis", backref="appointment_lab_analysis", lazy=True)

  def __repr__(self):
    return f"{self.patient_id}"
