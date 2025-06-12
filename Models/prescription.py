from Models.base_model import db, BaseModel, get_local_time

class Prescription(BaseModel, db.Model):
  __tablename__ = "prescription"
  patient_id = db.Column(db.Integer(), db.ForeignKey("patient.id"))
  appointment_id = db.Column(db.Integer(), db.ForeignKey("appointment.id"))
  note = db.Column(db.Text())
  is_active = db.Column(db.Boolean(), default=True)
  date_created = db.Column(db.DateTime(), default=get_local_time())
  date_closed = db.Column(db.DateTime())
  total = db.Column(db.Integer(), default=0)
  prescription_details = db.relationship("PrescriptionDetails", backref="prescription_info", lazy=True)
  payment = db.relationship("Payment", backref="prescription_payment", lazy=True)

  def __repr__(self):
    return f"{self.patient_id} - {self.total}"

class PrescriptionDetails(BaseModel, db.Model):
  __tablename__ = "prescription_details"
  prescription_id = db.Column(db.Integer(), db.ForeignKey("prescription.id"))
  medicine_id = db.Column(db.Integer(), db.ForeignKey("medicine.id"))
  amount = db.Column(db.Integer(), default=0)

  def __repr__(self):
    return f"{self.prescription_id} - {self.medicine_id}, {self.amount}"
