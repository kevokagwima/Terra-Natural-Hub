from flask import Flask
from Models.base_model import db
from Models.diagnosis import *
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def update_diagnosis_month_date():
  diagnosis_details = DiagnosisDetails.query.all()
  print(diagnosis_details)
  try:
    for diagnosis_detail in diagnosis_details:
      diagnosis = Diagnosis.query.filter_by(id=diagnosis_detail.diagnosis_id).first()
      diagnosis_detail.month_created = int(diagnosis.date_created.strftime("%m"))
      db.session.commit()
    print("Diagnosis updated successfully")
  except Exception as e:
    print(str(e))

if __name__ == "__main__":
  with app.app_context():
    update_diagnosis_month_date()
