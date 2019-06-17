from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email
from user import User
from app import session

class SignUpForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Sign up')
  
  def validate_email(self, email):
    user = session.query(User).filter_by(email=email.data).first()
    if user is not None:
      raise ValidationError('This email is already used')

class SignInForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Sign in')
