from functools import wraps
from flask import request, redirect, flash
from flask_login import current_user

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
