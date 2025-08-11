from app import create_app
from dotenv import load_dotenv

load_dotenv(override=True)

flask_app = create_app()
celery_app = flask_app.extensions["celery"]
