from flask import Flask
from flask_bcrypt import Bcrypt
from Models.base_model import db
from Models.users import Patients
from Models.diseases import Disease
from Models.medicine import Medicine, Inventory
from Models.users import Staff, Role
from config import Config
import csv

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt = Bcrypt()

def add_patients():
  user_file = open("clients.csv")
  read_files = csv.reader(user_file)

  for fname, lname, age, gender, phone1, phone2 in read_files:
    new_patient = Patients(
      first_name = fname,
      last_name = lname,
      phone_number_1 = phone1,
      phone_number_2 = phone2,
      age = age,
      gender = gender,
      clinic_id = 1,
    )
    db.session.add(new_patient)
    db.session.commit()

def add_diseases():
  user_file = open("Disease2.csv")
  read_files = csv.reader(user_file)

  for names in read_files:
    for name in names:
      new_disease = Disease(
        name = name
      )
      db.session.add(new_disease)
      db.session.commit()
    
  print("Diseases Added")

def add_medicine():
  user_file = open("Price list.csv")
  read_files = csv.reader(user_file)

  for name, price in read_files:
    new_medicine = Medicine(
      name = name,
      price = price,
    )
    db.session.add(new_medicine)
    db.session.commit()
  print("Medicines Added")

def add_admin():
  new_staff = Staff(
    first_name = "Kevin",
    last_name = "Maina",
    email = "test@gmail.com",
    phone = "0787654320",
    role_id = Role.query.filter_by(name="Admin").first().id,
    password = bcrypt.generate_password_hash("111111").decode("utf-8"),
  )
  db.session.add(new_staff)
  db.session.commit()
  print(f"New Admin addedd")

if __name__ == "__main__":
  with app.app_context():
    # add_patients()
    add_diseases()
    add_medicine()
    add_admin()
