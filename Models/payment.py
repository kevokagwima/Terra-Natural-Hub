from Models.base_model import db, BaseModel, get_local_time

class Payment(BaseModel, db.Model):
  __tablename__ = "payment"
  amount = db.Column(db.Integer(), default=0)
  is_pending = db.Column(db.Boolean(), default=False)
  is_completed = db.Column(db.Boolean(), default=False)
  is_canceled = db.Column(db.Boolean(), default=False)
  date_paid = db.Column(db.DateTime(), default=get_local_time())
  prescription_id = db.Column(db.Integer(), db.ForeignKey("prescription.id"))
  patient_id = db.Column(db.Integer(), db.ForeignKey("patient.id"))
  clinic_id = db.Column(db.Integer(), db.ForeignKey("clinic.id"))

  def __repr__(self):
    return f"{self.amount} - {self.prescription_id}"
  
  def to_dict(self):
    return {
      'payment_id': self.unique_id,
      'amount': self.amount,
      'date_paid': self.date_paid,
      'is_completed': self.is_completed,
    }
