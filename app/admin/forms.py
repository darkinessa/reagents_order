from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import Email, EqualTo, DataRequired, ValidationError
from app.auth.models import User



class EditProfileForm(FlaskForm):
    pass