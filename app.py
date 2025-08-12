from flask import Flask, flash
from flask_login import LoginManager, login_manager
from Models.base_model import db
from Models.users import Staff
from flask_migrate import Migrate
from config import Config
from flask_bcrypt import Bcrypt
from Errors.handlers import errors
from Admin.routes import admin, cache, celery_init_app
from Auth.routes import auth

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  db.init_app(app)
  migrate = Migrate(app, db)
  cache.init_app(app)
  celery_init_app(app)

  app.register_blueprint(errors)
  app.register_blueprint(admin)
  app.register_blueprint(auth)
  login_manager = LoginManager()

  login_manager.blueprint_login_views = {
    'admin': '/auth/signin',
  }
  login_manager.login_message="Please Login or Sign Up to access this page"
  login_manager.login_message_category="info"
  login_manager.refresh_view = "/auth/signin"
  login_manager.needs_refresh_message = "Your account has been inactive for a long time please authenticate yourself again."
  login_manager.needs_refresh_message_category = "info"

  login_manager.init_app(app)
  bcrypt = Bcrypt()

  @login_manager.user_loader
  def load_user(user_id):
    try:
      return Staff.query.filter_by(unique_id=user_id).first()
    except:
      flash("Failed to login the user", "danger")
  
  return app

if __name__ == "__main__":
  app = create_app()
  app.run(debug=True)
