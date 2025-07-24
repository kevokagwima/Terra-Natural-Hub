from Models.base_model import db, BaseModel, get_local_time

class Diagnosis(BaseModel, db.Model):
  __tablename__ = "diagnosis"
  patient_id = db.Column(db.Integer(), db.ForeignKey("patient.id"))
  clinic_id = db.Column(db.Integer(), db.ForeignKey("clinic.id"))
  appointment_id = db.Column(db.Integer(), db.ForeignKey("appointment.id"))
  note = db.Column(db.Text())
  is_active = db.Column(db.Boolean(), default=True)
  date_created = db.Column(db.DateTime(), default=get_local_time())
  date_closed = db.Column(db.DateTime())
  diagnosis_details = db.relationship("DiagnosisDetails", backref="diagnosis_info", lazy=True)

  def __repr__(self):
    return f"{self.patient_id}"

class DiagnosisDetails(BaseModel, db.Model):
  __tablename__ = "diagnosis_details"
  diagnosis_id = db.Column(db.Integer(), db.ForeignKey("diagnosis.id"))
  disease_id = db.Column(db.Integer(), db.ForeignKey("disease.id"))
  month_created = db.Column(db.Integer(), default=int(get_local_time().strftime("%m")))
  clinic_id = db.Column(db.Integer(), db.ForeignKey("clinic.id"))

  def __repr__(self):
    return f"{self.id}"
