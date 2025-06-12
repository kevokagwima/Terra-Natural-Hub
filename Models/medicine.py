from Models.base_model import db, BaseModel

class Medicine(BaseModel, db.Model):
  __tablename__ = "medicine"
  name = db.Column(db.String(200), nullable=False)
  price = db.Column(db.Integer(), default=0)
  quantity = db.Column(db.Integer(), default=0)
  prescription = db.relationship("PrescriptionDetails", backref="prescribed_medicine", lazy=True)

  def __repr__(self):
    return f"{self.name} - {self.price}"
