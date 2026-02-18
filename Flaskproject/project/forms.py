from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from project.models import User

class UniqueUsername:
    """Custom validator to check if username is unique."""

    def __init__(self, message=None):
        if not message:
            message = 'Username is already taken. Please choose a different username.'
        self.message = message

    def __call__(self, form, field):
        existing_user = User.query.filter_by(username=field.data).first()
        if existing_user:
            raise ValidationError(self.message)

class UniqueEmail:
    """Custom validator to check if email address is unique."""

    def __init__(self, message=None):
        if not message:
            message = 'Email address is already in use. Please choose a different email address.'
        self.message = message

    def __call__(self, form, field):
        existing_email = User.query.filter_by(email_address=field.data).first()
        if existing_email:
            raise ValidationError(self.message)

class RegisterForm(FlaskForm):
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired(), UniqueUsername()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired(), UniqueEmail()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='CREATE ACCOUNT')


class LoginForm(FlaskForm):
   username = StringField(label='User Name:', validators=[DataRequired()])
   password = PasswordField(label='Password:', validators=[DataRequired()])
   submit = SubmitField(label='Sign in')