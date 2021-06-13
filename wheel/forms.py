from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField, FileAllowed

from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, RadioField, SelectField, DateTimeField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo

from werkzeug.utils import secure_filename

from wheel.models import Event

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
    image = FileField('Event Image', validators=[FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])
    status = SelectField('Status', choices=[('inactive', 'Inactive'), ('upcoming', 'Upcoming'), ('booked out', 'Booked Out'), ('cancelled', 'Cancelled')])
    category = SelectField('Category')
    newcategory = StringField('New Category')
    tickets = StringField('Tickets') # note: you don't have to use this in the template. the Javascript on the create.html page adds this on submit. but it does have to be here

    submit = SubmitField("Create")



class BookEventForm(FlaskForm):
    ticket = RadioField('Tickets', coerce=int, validators=[InputRequired()])
    qty = IntegerField('Number of Gondolas', default=1, validators=[InputRequired()])
    price = IntegerField('Total Price', default=0, validators=[InputRequired()])
    submit = SubmitField("Book now")



class PostReviewForm(FlaskForm):
    text = TextAreaField('Review', [InputRequired()])
    submit = SubmitField("Post review")



class SearchForm(FlaskForm):
    search = StringField('Search')
    category = SelectField('Category')