from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField
from wtforms.validators import Length, DataRequired, Optional

class AddPatientForm(FlaskForm):
  first_name = StringField('First Name', validators=[DataRequired(message="First Name required"), Length(max=50)])
  last_name = StringField('Last Name', validators=[DataRequired(message="Last Name required"), Length(max=50)])
  age = IntegerField('Age', validators=[DataRequired(message="Age Required")])
  gender = SelectField('Gender', choices=[('', 'Select Gender'), ('male', 'Male'), ('female', 'Female')
  ], validators=[DataRequired(message="Gender field required")])
  phone_number_1 = StringField('Primary Phone', validators=[DataRequired(message="Phone Number required"), Length(max=20)])
  phone_number_2 = StringField('Secondary Phone', validators=[Optional(), Length(max=20)])
  region = StringField('Region', validators=[Optional(), Length(max=20)])
  district = StringField('District', validators=[Optional(), Length(max=30)])

class LabAnalysisForm(FlaskForm):
  test = TextAreaField('Test Conducted', validators=[DataRequired(message="Test field required")])
  result = TextAreaField('Test Results', validators=[DataRequired(message="Result field required")])

class DiagnosisForm(FlaskForm):
  diagnosis = SelectField('Diagnose Disease', choices=[], validators=[DataRequired(message="Diagnosis field required")])
  note = TextAreaField('Note', validators=[Optional()])

class PrescriptionForm(FlaskForm):
  prescription = SelectField('Prescribe Medication', choices=[], validators=[DataRequired(message="Prescription field required")])
  note = TextAreaField('Note', validators=[Optional()])
