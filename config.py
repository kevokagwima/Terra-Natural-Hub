import os

class Config:
  SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root:Hunter9039@localhost/terra"
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SESSION_PERMANENT = False
  SESSION_TYPE = "filesystem"
  SECRET_KEY = os.environ.get("SECRET_KEY")
  CACHE_TYPE = "SimpleCache"
  CACHE_DEFAULT_TIMEOUT = 300