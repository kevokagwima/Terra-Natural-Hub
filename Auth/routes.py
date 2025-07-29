from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user, fresh_login_required
from Models.base_model import db
from Models.users import Staff, Role
from Models.clinic import Clinic
from .form import StaffRegistrationForm, StaffLoginForm
from Utils.email import send_email
import secrets, string

auth = Blueprint("auth", __name__, url_prefix="/auth")

@auth.route("/signup", methods=["POST"])
def signup():
  form = StaffRegistrationForm()
  form.role.choices = [(role.unique_id, role.name) for role in Role.query.all()]
  staff_count = Staff.query.count()
  form.branch.choices = [(clinic.unique_id, clinic.name) for clinic in Clinic.query.all()]
  try:
    if form.validate_on_submit():
      if staff_count < 14:
        new_staff = Staff(
          first_name = form.first_name.data,
          last_name = form.last_name.data, 
          role_id = Role.query.filter_by(unique_id=form.role.data).first().id, 
          clinic_id = Clinic.query.filter_by(unique_id=form.branch.data).first().id, 
          phone = form.phone_number.data, 
          email = form.email_address.data, 
          passwords = generate_password(),      
        )
        db.session.add(new_staff)
        db.session.commit()
        flash("Account created successfully", "success")
        return redirect(url_for('admin.dashboard'))
      else:
        flash("You've reached maximum number of staff allowed", category="warning")
        return redirect(url_for('admin.dashboard'))

    if form.errors != {}:
      for err_msg in form.errors.values():
        flash(f"{err_msg}", "danger")
      return redirect(url_for('admin.dashboard'))

  except Exception as e:
    flash(f"{str(e)}", "danger")

  return redirect(url_for('admin.dashboard'))

def generate_password(length=12):
  """Generate a secure random password with letters, numbers, and symbols"""
  chars = (
    string.ascii_letters.translate({ord(c): None for c in 'Il1O0'}) +  # Remove ambiguous chars
    string.digits.translate({ord(c): None for c in '01'}) +
    '!@#$%^&*_+-='
  )
  return ''.join(secrets.choice(chars) for _ in range(length))

@auth.route("/signin", methods=["POST","GET"])
def signin():
  form = StaffLoginForm()
  try:
    if form.validate_on_submit():
      staff = Staff.query.filter_by(email=form.email_address.data).first()
      if not staff:
        flash("No staff with that email address", "danger")
        return redirect(url_for("auth.signin"))
      elif staff and staff.check_password_correction(attempted_password=form.password.data):
        login_user(staff, remember=True)
        flash("Login successfull", "success")
        next = request.args.get("next")
        send_email()
        return redirect(next or url_for("admin.select_branch"))
      else:
        flash("Invalid credentials", "danger")
        return redirect(url_for("auth.signin"))

    if form.errors != {}:
      for err_msg in form.errors.values():
        flash(f"{err_msg}", "danger")
        return redirect(url_for("auth.signin"))

  except Exception as e:
    flash(f"{str(e)}", "danger")
    return redirect(url_for("auth.signin"))

  context = {
    "form": form
  }

  return render_template("Auth/login.html", **context)

@auth.route("/logout")
@login_required
@fresh_login_required
def logout():
  try:
    logout_user()
    flash("Logout successful", "success")
    return redirect(url_for("auth.signin"))
  except Exception as e:
    flash(f"{str(e)}", "danger")
    return redirect(request.referrer)
