from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from app import engine, session
from flask_login import UserMixin

Base = declarative_base()

class User(UserMixin, Base):
  __tablename__ = 'users_'
  id = Column(Integer, primary_key=True)
  email = Column(String(64))
  password_hash = Column(String(128))
  is_active = Column(Boolean)
    
  def __init__(self, email, is_active):
    self.email = email
    self.is_active = is_active

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

Base.metadata.create_all(engine)
session.query(User).delete()

