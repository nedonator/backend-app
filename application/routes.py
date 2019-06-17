from flask import render_template, flash, redirect, url_for
from forms import SignUpForm, SignInForm
from user import User
from flask_login import current_user, login_user, logout_user
from app import app, session
import pika
import json
from itsdangerous import URLSafeTimedSerializer

def send_email(email):
  conn_params = pika.ConnectionParameters(host='rabbitmq', port=5672)
  connection = pika.BlockingConnection(conn_params)
  channel = connection.channel()
  channel.queue_declare(queue='rabbit-queue')
  token = URLSafeTimedSerializer(app.config['SECRET_KEY']).dumps(email, salt=app.config['SALT'])
  confirm_url = url_for('confirm_email', token=token, _external=True)
  json_map = json.dumps({"email": email, "confirm_url": confirm_url})
  channel.basic_publish(exchange='', routing_key='rabbit-queue', body=json_map)
  connection.close()

@app.route('/')
@app.route('/index')
def index():
  if not current_user.is_authenticated:
    return redirect(url_for('login'))
  return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = SignInForm()
  if form.validate_on_submit():
    user = session.query(User).filter_by(email=form.email.data).first()
    if user is None:
      flash('Email is not registred')
      return redirect(url_for('login'))
    elif not user.check_password(form.password.data):
      flash('Wrong password')
      return redirect(url_for('login'))
    elif not user.is_active:
      flash('You have to confirm your account. Check your email')
      send_email(user.email)
      return redirect(url_for('login'))
    login_user(user)
    return redirect(url_for('index'))
  return render_template('login.html', title='Sign in', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/registration', methods=['GET', 'POST'])
def registration():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = SignUpForm()
  if form.validate_on_submit():
    user = User(email=form.email.data, is_active=False)
    user.set_password(form.password.data)
    session.add(user)
    session.commit()
    send_email(user.email)
    flash('A confirmation email has been sent', 'success')
    return redirect(url_for('login'))
  return render_template('register.html', title='Sign up', form=form)

@app.route('/confirm/<token>')
def confirm_email(token):
  try:
    email = URLSafeTimedSerializer(app.config['SECRET_KEY']).loads(token, salt=app.config['SALT'], max_age=80000)
  except:
    flash('The confirmation link is wrong. Try to log in in order to get a new one', 'danger')
  user = session.query(User).filter_by(email=email).first()
  user.is_active = True
  session.add(user)
  session.commit()
  flash('Your account is now active', 'success')
  return redirect(url_for('index'))
