from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, RadioField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField("Email address", validators=[Email("Please enter a valid email")])
    
    password = PasswordField("Password", validators=[InputRequired(),
            EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    submit = SubmitField("Register")


class CreateEventForm(FlaskForm):
    # TODO: add all the neccessary fields
    submit = SubmitField("Create")


class BookEventForm(FlaskForm):
    ticket = RadioField('Tickets', coerce=int, validators=[InputRequired()])
    qty = IntegerField('Number of Gondolas', default=1, validators=[InputRequired()])
    price = IntegerField('Total Price', default=0, validators=[InputRequired()])
    submit = SubmitField("Book now")


class PostReviewForm(FlaskForm):
    # TODO: add all the neccessary fields
    submit = SubmitField("Post review")


class SearchForm(FlaskForm):
    # TODO: add all the neccessary fields
    submit = SubmitField("Search")