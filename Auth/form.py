from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from Models.users import Staff

class StaffRegistrationForm(FlaskForm):
  first_name = StringField(label="First Name", validators=[DataRequired(message="First Name field required")])
  last_name = StringField(label="Last Name", validators=[DataRequired(message="Last Name field required")])
  email_address = EmailField(label="Email Address", validators=[Email(), DataRequired(message="Email Address field required")])
  phone_number = StringField(label="Phone Number", validators=[Length(min=10, max=10, message="Invalid Phone Number"), DataRequired(message="Phone Number field required")])
  role = SelectField(label="Select Role", choices=[], validators=[DataRequired(message="Role required")])
  branch = SelectField(label="Select Branch", choices=[], validators=[DataRequired(message="Branch required")])

  def validate_phone_number(self, phone_number_to_validate):
    phone_number = phone_number_to_validate.data
    if phone_number[0] != str(0):
      raise ValidationError("Invalid phone number. Phone number must begin with 0")
    elif phone_number[1] != str(7) and phone_number[1] != str(1):
      raise ValidationError("Invalid phone number. Phone number must begin with 0 followed by 7 or 1")
    elif Staff.query.filter_by(phone=phone_number_to_validate.data).first():
      raise ValidationError("Phone Number already exists, Please try another one")

  def validate_email_address(self, email_to_validate):
    email = Staff.query.filter_by(email=email_to_validate.data).first()
    if email:
      raise ValidationError("Email Address already exists, Please try another one")

class StaffLoginForm(FlaskForm):
  email_address = EmailField(label="Email Address", validators=[DataRequired(message="Email address field required")])
  password = PasswordField(label="Password", validators=[DataRequired(message="Password field required")])

class ResetPasswordForm(FlaskForm):
  email_address = EmailField(label="Email Address", validators=[DataRequired(message="Email address field required")])
  new_password = PasswordField(label="New Password", validators=[DataRequired(message="Password field required")])
  confirm_password = PasswordField(label="Confirm Password", validators=[EqualTo("new_password", message="Passwords do not match"), DataRequired(message="Confirm Password field required")])
