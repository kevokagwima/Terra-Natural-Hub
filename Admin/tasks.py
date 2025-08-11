from celery import shared_task
from Models.base_model import db
from Models.users import Patients
from Models.clinic import Clinic
from Models.medicine import Inventory, Medicine
import csv

@shared_task
def populate_inventory(branch_id):
  try:
    clinic = Clinic.query.filter_by(unique_id=branch_id).first()
    medicines = Medicine.query.all()
    clinic_inventory = Inventory.query.filter_by(clinic_id=clinic.id).all()
    if len(medicines) != len(clinic_inventory):
      for medicine in medicines:
        existing_clinic_inventory = Inventory.query.filter_by(clinic_id=clinic.id, medicine_id=medicine.id).first()
        if not existing_clinic_inventory:
          new_inventory = Inventory(
            clinic_id = clinic.id,
            medicine_id = medicine.id,
            quantity = 100
          )
          db.session.add(new_inventory)
          db.session.commit()
  except Exception as e:
    db.session.rollback()
    print(f"{str(e)}")

@shared_task
def populate_patients(branch_id):
  try:
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
        clinic_id = Clinic.query.filter_by(unique_id=branch_id).first().id,
      )
      db.session.add(new_patient)
      db.session.commit()
  except Exception as e:
    db.session.rollback()
    print(f"{str(e)}")

@shared_task
def update_inventory(branch_id):
  try:
    clinic = Clinic.query.filter_by(unique_id=branch_id).first()
    if clinic:
      clinic_inventory = Inventory.query.filter_by(clinic_id=clinic.id).all()
      for inventory in clinic_inventory:
        db.session.delete(inventory)
        db.session.commit()
      clinic_patients = Patients.query.filter_by(clinic_id=clinic.id).all()
      for patient in clinic_patients:
        db.session.delete(patient)
        db.session.commit()
  except Exception as e:
    db.session.rollback()
    print(f"{str(e)}")
