from dotenv import load_dotenv
import os

load_dotenv()

class Config:
  SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root:Hunter9039@localhost/terra"
  # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SESSION_PERMANENT = False
  SESSION_TYPE = "filesystem"
  SECRET_KEY = os.environ.get("SECRET_KEY")
  CACHE_TYPE = "SimpleCache"
  CACHE_REDIS_PORT = 6379
  CACHE_DEFAULT_TIMEOUT = 300
  CELERY = {
    "broker_url": "redis://localhost:6379",
    "result_backend": "redis://localhost:6379",
  }