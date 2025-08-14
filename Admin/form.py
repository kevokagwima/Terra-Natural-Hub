from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import Length, DataRequired, Optional, NumberRange, EqualTo
from Models.users import Staff

region_districts = {
  "Arusha": ["Monduli", "Arusha", "Arumeru", "Karatu", "Longido", "Ngorongoro"],
  "Dar es Salaam": ["Ilala", "Kinondoni", "Temeke", "Kigamboni", "Ubungo"],
  "Dodoma": ["Bahi", "Chamwino", "Chemba", "Dodoma", "Kondoa", "Kongwa", "Mpwapwa"],
  "Geita": ["Bukombe", "Chato", "Geita", "Mbogwe", "Nyang'hwale"],
  "Iringa": ["Iringa", "Kilolo", "Mafinga Town", "Mufindi"],
  "Kagera": ["Biharamulo", "Bukoba", "Karagwe", "Kyerwa", "Missenyi", "Muleba", "Ngara"],
  "Katavi": ["Mlele", "Mpanda"],
  "Kigoma": ["Buhigwe", "Kakonko", "Kasulu", "Kibondo", "Kigoma", "Uvinz"],
  "Kilimanjaro": ["Hai", "Moshi", "Mwanga", "Rombo", "Same", "Siha"],
  "Lindi": ["Kilwa", "Lindi", "Liwale", "Nachingwea", "Ruangwa"],
  "Manyara": ["Babati", "Hanang", "Kiteto", "Mbulu", "Simanjiro"],
  "Mara": ["Bunda", "Butiama", "Musoma", "Rorya", "Serengeti", "Tarime"],
  "Mbeya": ["Busokelo", "Chunya", "Kyela", "Mbarali", "Mbeya", "Rungwe"],
  "Mororgoro": ["Gairo", "Kilombero", "Kilosa", "Morogoro", "Mvomero", "Ulanga"],
  "Mtwara": ["Masasi", "Mtwara", "Nanyumbu", "Newala", "Tandahimba"],
  "Mwanza": ["Ilemela", "Kwimba", "Magu", "Misungwi", "Nyamagana", "Sengerema", "Ukerewe"],
  "Njombe": ["Ludewa", "Makambako Town", "Makete", "Njombe", "Wanging'ombe"],
  "Pwani": ["Bagamoyo", "Kibaha", "Kisarawe", "Mafia", "Mkuranga", "Rufiji"],
  "Rukwa": ["Kalambo", "Nkasi", "Sumbawanga"],
  "Ruvuma": ["Mbinga", "Namtumbo", "Nyasa", "Songea", "Tunduru"],
  "Shinyanga": ["Kahama", "Kishapu", "Shinyanga"],
  "Simiyu": ["Bariadi", "Busega", "Itilima", "Maswa", "Meat"],
  "Singida": ["Ikungi", "Iramba", "Manyoni", "Mkalama", "Singida"],
  "Songwe": ["Ileje", "Mbozi", "Momba", "Songwe"],
  "Tabora": ["Igunga", "Kaliua", "Nzega", "Sikonge", "Tabora", "Uyu"],
  "Tanga": ["Handeni", "Kilindi", "Korogwe", "Lushoto", "Mkinga", "Muheza", "Pangani", "Tanga"],
  "Zanzibar": ["Zanzibar Central/South", "Zanzibar North", "Zanzibar Urban/West"]
}

class AddPatientForm(FlaskForm):
  first_name = StringField('First Name', validators=[DataRequired(message="First Name required"), Length(max=150)])
  last_name = StringField('Last Name', validators=[DataRequired(message="Last Name required"), Length(max=150)])
  age = IntegerField('Age', validators=[DataRequired(message="Age Required")])
  gender = SelectField('Gender', choices=[('', 'Select Gender'), ('male', 'Male'), ('female', 'Female')
  ], validators=[DataRequired(message="Gender field required")])
  phone_number_1 = StringField('Primary Phone', validators=[DataRequired(message="Phone Number required"), Length(max=20)])
  phone_number_2 = StringField('Secondary Phone', validators=[Optional(), Length(max=20)])
  region = SelectField('Region', choices=[], validators=[Optional()])
  district = SelectField('District', choices=[], validators=[Optional()])
  location = StringField('Location', validators=[Optional(), Length(max=50)])

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # Populate regions
    self.region.choices = [(r, r) for r in region_districts.keys()]
      
  def validate(self, extra_validators=None):
    # First run basic validations
    if not super().validate():
      return False
    
    # Custom validation: Check if district belongs to region
    selected_region = self.region.data
    selected_district = self.district.data
    
    if not selected_district:
      return True
    
    if selected_district not in region_districts.get(selected_region, []):
      self.district.errors.append(f"Invalid district for {selected_region} region")
      return False

    return True

class AddMedicineForm(FlaskForm):
  name = StringField('Medicine Name', validators=[DataRequired(message="Medicine name field required"), Length(max=200)])
  price = IntegerField('Medicine Price', validators=[DataRequired(message="Medicine price field required"), NumberRange(min=1, message="Minimum price is Tsh 1")])
  quantity = IntegerField('Medicine Quantity', validators=[Optional(), NumberRange(min=1, message="Minimum amount is 1")])
  # all_clinic = BooleanField("Add to all branches", default=True)

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

class AddClinicForm(FlaskForm):
  name = StringField('Clinic Name', validators=[DataRequired(message="Clinic Name required"), Length(max=150)])
  branch_type = SelectField(label="Branch Type", choices=[("","Select Branch Type"),("Headquarters","Headquarters"), ("Other","Other")], validators=[DataRequired(message="Branch Type required")])
  region = StringField('Region', validators=[DataRequired(message="Region field required")])
  district = StringField('District', validators=[DataRequired(message="District field required")])

class UpdatedPasswordForm(FlaskForm):
  new_password = PasswordField("New Password", validators=[DataRequired(message="New password field is required")])
  confirm_password = PasswordField("Confirm Password", validators=[EqualTo("new_password", message="Passwords do not match"), DataRequired(message="Confirm password field is required")])
