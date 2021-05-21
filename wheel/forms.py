from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField("Email address", validators=[Email("Please enter a valid email")])
    
    password = PasswordField("Password", validators=[InputRequired(),
            EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    submit = SubmitField("Register")


class CreateEventForm(FlaskForm):
    submit = SubmitField("Create")


class BookEventForm(FlaskForm):
    submit = SubmitField("Pay now")