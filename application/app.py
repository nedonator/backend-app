from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
engine = create_engine(app.config['DATABASE_URI'], echo = False)
Session = sessionmaker(bind=engine)
session = Session()

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return session.query(User).get(int(id))

import routes
from user import User
