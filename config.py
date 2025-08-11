from dotenv import load_dotenv
import os

load_dotenv()

class Config:
  SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SESSION_PERMANENT = False
  SESSION_TYPE = "filesystem"
  SECRET_KEY = os.environ.get("SECRET_KEY")
  CACHE_TYPE = "RedisCache"
  CELERY = {
    "broker_url": os.environ.get("REDIS_URL"),
    "result_backend": os.environ.get("REDIS_URL")
  }