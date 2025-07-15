from Models.base_model import db, BaseModel, get_local_time

class LabAnalysis(BaseModel, db.Model):
  __tablename__ = "lab_analysis"
  patient_id = db.Column(db.Integer(), db.ForeignKey("patient.id"))
  appointment_id = db.Column(db.Integer(), db.ForeignKey("appointment.id"))
  clinic_id = db.Column(db.Integer(), db.ForeignKey("clinic.id"))
  is_active = db.Column(db.Boolean(), default=True)
  is_approved = db.Column(db.Boolean(), default=False)
  date_created = db.Column(db.DateTime(), default=get_local_time())
  date_approved = db.Column(db.DateTime())
  lab_analysis_details = db.relationship("LabAnalysisDetails", backref="lab_analysis", lazy=True)

  def __repr__(self):
    return f"{self.patient_id}"

class LabAnalysisDetails(BaseModel, db.Model):
  __tablename__ = "lab_analysis_details"
  lab_analysis_id = db.Column(db.Integer(), db.ForeignKey("lab_analysis.id"))
  test = db.Column(db.Text(), nullable=False)
  result = db.Column(db.Text(), nullable=False)

  def __repr__(self):
    return f"{self.lab_analysis_id}"
