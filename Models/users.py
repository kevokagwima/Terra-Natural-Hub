from Models.base_model import db, BaseModel, UserBaseModel
from Models.diagnosis import Diagnosis
from Models.prescription import Prescription
from Models.payment import Payment
from Models.appointment import Appointment
from Models.clinic import Clinic
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class Role(BaseModel, db.Model):
  __tablename__ = 'role'
  name = db.Column(db.String(20), nullable=False)
  user = db.relationship("Staff", backref="staff_role", lazy=True)

  def __repr__(self):
    return f"{self.name}"

class Staff(BaseModel, UserBaseModel, UserMixin, db.Model):
  __tablename__ = 'staff'
  role_id = db.Column(db.Integer(), db.ForeignKey("role.id"))
  clinic_id = db.Column(db.Integer(), db.ForeignKey("clinic.id"))

  @property
  def passwords(self):
    return self.passwords

  @passwords.setter
  def passwords(self, plain_text_password):
    self.password = bcrypt.generate_password_hash(plain_text_password).decode("utf-8")

  def check_password_correction(self, attempted_password):
    return bcrypt.check_password_hash(self.password, attempted_password)
  
  def __repr__(self):
    return f"{self.first_name} {self.last_name}"

class Patients(BaseModel, db.Model):
  __tablename__ = "patient"
  first_name = db.Column(db.String(50), nullable=False)
  last_name = db.Column(db.String(50), nullable=False)
  age = db.Column(db.Integer())
  gender = db.Column(db.String(6))
  phone_number_1 = db.Column(db.String(20))
  phone_number_2 = db.Column(db.String(20))
  address_id = db.Column(db.Integer(), db.ForeignKey("patient_address.id"))
  payment = db.relationship("Payment", backref="clinic_payment", lazy=True)
  clinic_id = db.Column(db.Integer(), db.ForeignKey("clinic.id"))
  diagnosis = db.relationship("Diagnosis", backref="patient_diagnosis", lazy=True)
  prescription = db.relationship("Prescription", backref="patient_prescription", lazy=True)
  payment = db.relationship("Payment", backref="patient_payment", lazy=True)
  appointment = db.relationship("Appointment", backref="patient_appointment", lazy=True)
  lab_analysis = db.relationship("LabAnalysis", backref="patient_labtest", lazy=True)

  def __repr__(self):
    return f"{self.first_name} - {self.last_name}"
  
  def to_dict(self):
    return {
      'patient_id': self.unique_id,
      'first_name': self.first_name,
      'last_name': self.last_name,
      'age': self.age,
      'gender': self.gender,
      'phone_number_1': self.phone_number_1,
      'phone_number_2': self.phone_number_2,
    }

class PatientAddress(BaseModel, db.Model):
  __tablename__ = "patient_address"
  region = db.Column(db.String(20))
  district = db.Column(db.String(30))
  location = db.Column(db.String(100))
  patient = db.relationship("Patients", backref="patient_address", lazy=True)

  def __repr__(self):
    return f"{self.region} - {self.district}"
  
  def to_dict(self):
    return {
      'region': self.region,
      'district': self.district,
      'location': self.location
    }
