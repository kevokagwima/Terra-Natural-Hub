from flask import Blueprint, render_template, redirect, url_for, flash, request, session, make_response
from flask_login import login_required, login_user, logout_user, fresh_login_required, current_user
from flask_bcrypt import Bcrypt
from Models.base_model import db
from Models.users import Staff, Role
from Models.clinic import Clinic
from .form import StaffRegistrationForm, StaffLoginForm, ResetPasswordForm
from Admin.form import UpdatedPasswordForm
from Admin.routes import cache, CachedResponse
from Utils.email import send_email
from Utils.notification_service import NotificationService
from decorator import role_required
import secrets, string

auth = Blueprint("auth", __name__, url_prefix="/auth")
bcrypt = Bcrypt()

@auth.route("/signup", methods=["POST"])
@login_required
@fresh_login_required
@role_required(["Admin"])
def signup():
  form = StaffRegistrationForm()
  form.role.choices = [(role.unique_id, role.name) for role in Role.query.all()]
  staff_count = Staff.query.count()
  form.branch.choices = [(clinic.unique_id, clinic.name) for clinic in Clinic.query.all()]
  try:
    cache.clear()
    if form.validate_on_submit():
      generated_password = generate_password()
      if staff_count < 14:
        new_staff = Staff(
          first_name = form.first_name.data,
          last_name = form.last_name.data, 
          role_id = Role.query.filter_by(unique_id=form.role.data).first().id, 
          clinic_id = Clinic.query.filter_by(unique_id=form.branch.data).first().id, 
          phone = form.phone_number.data, 
          email = form.email_address.data, 
          passwords = generated_password,      
        )
        db.session.add(new_staff)
        db.session.commit()
        flash("Staff account created successfully", "success")
        email_message = {
          "receiver": f"{new_staff.email}",
          "subject": "TNH Account",
          "message": f"<h2>Dear, {new_staff.first_name} {new_staff.last_name}</h2><p>Your TNH account has been created successfully. A temporary password has been created for your account. After login you can update your password to your password of choice.</p><br><p>Here's your temporary password: {generated_password}<b></b></p><br><h4>Welcome to the team</h4>"
        }
        send_email(**email_message)
        NotificationService.create_new_staff_notification(
          new_staff.id,
          f"{new_staff.staff_role.name}",
          f"{new_staff.first_name} {new_staff.last_name}",
        )
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

def generate_password(length=15):
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
  if form.validate_on_submit():
    cache.clear()
    try:
      staff = Staff.query.filter_by(email=form.email_address.data).first()
      if not staff:
        flash("No staff with that email address", "danger")
        return redirect(url_for("auth.signin"))
      elif staff and staff.check_password_correction(attempted_password=form.password.data):
        login_user(staff, remember=True)
        flash("Login successfull", "success")
        if current_user.staff_role.name == "Admin":
          return redirect(url_for("admin.clinic_branches"))
        else:
          session["clinic_id"] = current_user.clinic_id
          return redirect(url_for("admin.dashboard"))
      else:
        flash("Invalid credentials", "danger")
        return redirect(url_for("auth.signin"))

    except Exception as e:
      flash(f"{str(e)}", "danger")
      return redirect(url_for("auth.signin"))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", "danger")
      return redirect(url_for("auth.signin"))

  context = {
    "form": form
  }

  return CachedResponse(
    response = make_response(render_template("Auth/login.html", **context)),
    timeout=600
  )

@auth.route("/update-password", methods=["POST"])
@login_required
@fresh_login_required
def update_password():
  cache.clear()
  form = UpdatedPasswordForm()
  try:
    if form.validate_on_submit():
      staff = Staff.query.filter_by(email=current_user.email).first()
      if not staff:
        flash("No staff with that email address", "danger")
      else:
        staff.password = bcrypt.generate_password_hash(form.new_password.data).decode("utf-8")
        db.session.commit()
        flash("Password updated successfully", "success")
      
      return redirect(request.referrer)

    if form.errors != {}:
      for err_msg in form.errors.values():
        flash(f"{err_msg}", "danger")
        return redirect(request.referrer)

  except Exception as e:
    flash(f"{str(e)}", "danger")
    return redirect(request.referrer)

  return redirect(request.referrer)

@auth.route("/reset-password", methods=["POST", "GET"])
def reset_password():
  form = ResetPasswordForm()
  if form.validate_on_submit():
    cache.clear()
    try:
      user = Staff.query.filter_by(email=form.email_address.data).first()
      if user:
        if user.check_password_correction(attempted_password=form.new_password.data):
          flash("New password cannot be same as old", category="danger")
        else:
          user.password = bcrypt.generate_password_hash(form.new_password.data).decode("utf-8")
          db.session.commit()
          flash("Your password has been reset successfully", category="success")
          return redirect(url_for("auth.signin"))
      else:
        flash("No user with that email", category="danger")
        return redirect(url_for('auth.reset_password'))
      
    except Exception as e:
      flash(f"{str(e)}", "danger")
      return redirect(url_for('auth.reset_password'))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", category="danger")
      return redirect(url_for('auth.reset_password'))
  
  context = {
    "form": form
  }

  return CachedResponse(
    response = make_response(render_template("Auth/reset-password.html", **context)),
    timeout=600
  )

@auth.route("/logout")
@login_required
@fresh_login_required
def logout():
  try:
    cache.clear()
    logout_user()
    flash("Logout successful", "success")
    return redirect(url_for("auth.signin"))
  except Exception as e:
    flash(f"{str(e)}", "danger")
    return redirect(request.referrer)
