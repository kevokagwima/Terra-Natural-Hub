from Models.base_model import db, BaseModel

class Disease(BaseModel, db.Model):
  __tablename__ = "disease"
  name = db.Column(db.String(200), nullable=False)
  diagnosis_details = db.relationship("DiagnosisDetails", backref="diagnosed_disease", lazy=True)

  def __repr__(self):
    return f"{self.name}"
