from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, RadioField, SelectField, DateTimeField
from wtforms.fields.html5 import IntegerField
from wtforms.fields.simple import HiddenField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from werkzeug.utils import secure_filename
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'png', 'jpg', 'JPG', 'PNG'}

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField("Email address", validators=[Email("Please enter a valid email")])
    
    password = PasswordField("Password", validators=[InputRequired(),
            EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    submit = SubmitField("Register")


class CreateEventForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    desc = StringField('Description', validators=[InputRequired()])
    image = FileField('Event Image', validators=[FileRequired(message='Image can not be empty'),FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])
    status = SelectField('Status', choices=[('inactive', 'Inactive'), ('upcoming', 'Upcoming'), ('booked', 'Booked Out'), ('cancelled', 'Cancelled')])
    category = SelectField('Category')
    newcategory = StringField('New Category')
    tickets = StringField('Tickets') # note: you don't have to use this in the template. the Javascript on the create.html page adds this on submit. but it does have to be here

    # TODO: once this form is created we need to use the fields in template. Follow event.html as guide
    submit = SubmitField("Create")


class BookEventForm(FlaskForm):
    event = HiddenField('event')
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

class indexForm(FlaskForm):
    # trying to fix unidentified Form error
    submit = SubmitField("test")
