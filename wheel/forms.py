from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, RadioField, SelectField, DateTimeField
from wtforms.fields.html5 import IntegerField
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
    category = SelectField('Category', choices=[('category 1', 'category 1'), ('category 2', 'category 2'), ('category 3', 'category 3')])

    #ticket data needed, these are a bit weird because we have to make a lot of them, might have to do 2 forms

    #price = IntegerField('Price ($)', default=0, validators=[InputRequired()])
    #qty = IntegerField('Total number of gondolas', default=1, validators=[InputRequired()])
    #datetime = DateTimeField('Date/Time', validators=[InputRequired()])

    # TODO: need to add the tickets data and functionality so we can add a lot of them
    # TODO: once this form is created we need to use the fields in template. Follow event.html as guide
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