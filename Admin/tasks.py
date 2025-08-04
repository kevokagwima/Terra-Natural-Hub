from celery import shared_task
from Models.base_model import db
from Models.clinic import Clinic
from Models.medicine import Inventory, Medicine

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
