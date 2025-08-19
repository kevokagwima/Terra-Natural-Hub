from functools import wraps
from flask import request, redirect, flash, session, url_for
from flask_login import current_user
from Models.clinic import Clinic

def role_required(role_name):
  def decorator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
      if current_user.is_authenticated and current_user.staff_role.name in role_name:
        return f(*args, **kwargs)
      else:
        flash("You are not authorised to perform the specified action", "warning")
        return redirect(request.referrer)
    return decorated_function
  return decorator

def branch_required():
  def decorator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
      clinics = Clinic.query.count()
      if not "clinic_id" in session or clinics == 0:
        flash("You need to select a branch to perform the specified action", "warning")
        return redirect(url_for('admin.clinic_branches'))
      else:
        return f(*args, **kwargs)
    return decorated_function
  return decorator
