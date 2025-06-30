from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField
from wtforms.validators import Length, DataRequired, Optional, NumberRange

class AddPatientForm(FlaskForm):
  first_name = StringField('First Name', validators=[DataRequired(message="First Name required"), Length(max=50)])
  last_name = StringField('Last Name', validators=[DataRequired(message="Last Name required"), Length(max=50)])
  age = IntegerField('Age', validators=[DataRequired(message="Age Required")])
  gender = SelectField('Gender', choices=[('', 'Select Gender'), ('male', 'Male'), ('female', 'Female')
  ], validators=[DataRequired(message="Gender field required")])
  phone_number_1 = StringField('Primary Phone', validators=[DataRequired(message="Phone Number required"), Length(max=20)])
  phone_number_2 = StringField('Secondary Phone', validators=[Optional(), Length(max=20)])
  address = SelectField('Address', choices=[], validators=[Optional()])

class AddMedicineForm(FlaskForm):
  name = StringField('Medicine Name', validators=[DataRequired(message="Medicine name field required"), Length(max=200)])
  price = IntegerField('Medicine Price', validators=[DataRequired(message="Medicine price field required"), NumberRange(min=1, message="Minimum price is Tsh 1")])
  quantity = IntegerField('Medicine Quantity', validators=[Optional(), NumberRange(min=1, message="Minimum amount is 1")])

class AddDiseaseForm(FlaskForm):
  name = StringField('Disease Name', validators=[DataRequired(message="Disease name field required"), Length(max=200)])

class LabAnalysisForm(FlaskForm):
  test = TextAreaField('Test Conducted', validators=[DataRequired(message="Test field required")])
  result = TextAreaField('Test Results', validators=[DataRequired(message="Result field required")])

class DiagnosisForm(FlaskForm):
  diagnosis = SelectField('Diagnose Disease', choices=[], validators=[DataRequired(message="Diagnosis field required")])
  note = TextAreaField('Note (Optional)', validators=[Optional()])

class PrescriptionForm(FlaskForm):
  prescription = SelectField('Prescribe Medication', choices=[], validators=[DataRequired(message="Prescription field required")])
  note = TextAreaField('Note (Optional)', validators=[Optional()])

class FeedbackForm(FlaskForm):
  feedback = SelectField(label="Patient Feedback", choices=[("", "Select an option"), ("Recovered", "Recovered"), ("Not Recovered", "Not Recovered")], validators=[DataRequired(message="Feedback field is required")])
