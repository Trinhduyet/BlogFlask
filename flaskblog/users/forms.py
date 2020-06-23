from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,  username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'This username is taken! Please choose different one')

    def validate_email(self,  email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'This email is taken! Please choose different one')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ChangePasswordForm(FlaskForm):
    password = StringField('Password',
                           validators=[DataRequired(), Length(min=2, max=20)])
    re_password = StringField('Re-Password',
                           validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Update Account')

class RequestResetForm(FlaskForm):
    emailcode = StringField('Verity code', validators=[DataRequired()])
    submit = SubmitField('Submit')
  
