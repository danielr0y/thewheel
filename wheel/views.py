from itertools import groupby
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for
from flask.helpers import flash
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os, json
from .forms import CreateEventForm, BookEventForm, SearchForm, PostReviewForm, indexForm
from .models import Event, Booking, Ticket
from . import db 


main = Blueprint('main', __name__)
events = Blueprint('events', __name__, url_prefix='/events')


@events.route('/<int:id>/update')
def update(id):
    form = CreateEventForm() # TODO: create this form
    event = Event.get(id)

    # TODO: passing a form to this template does nothing
    # TODO: passing an event to this template does nothing
    # return render_template('create.html', form=form, event=event) 
    return render_template('create.html')



@events.route('/<int:id>')
def view(id):
    event = Event.get(id)
    bookform = BookEventForm()
    reviewform = PostReviewForm() # TODO: create this form

    # create radio field options from the tickets sorted by date
    bookform.ticket.choices = list(map(lambda ticket: (ticket.id, f'${ticket.price}'), event.tickets))

    # get a list of all possible times in order
    ticketssortedbytime = sorted(event.tickets, key=lambda ticket: ticket.datetime.strftime("%I:%M %p"))
    ticketsgroupedbytime = groupby(ticketssortedbytime, key=lambda ticket: ticket.datetime.strftime("%I:%M %p"))
    times = [time for time, _tickets in ticketsgroupedbytime]

    # get a list of ticket ids grouped by date
    ticketssortedbydate = sorted(event.tickets, key=lambda ticket: ticket.datetime)    
    ticketsgroupedbydate = groupby(ticketssortedbydate, key=lambda ticket: ticket.datetime.strftime("%d/%m/%Y"))
    dates = [[date, [time.id for time in times]] for date, times in ticketsgroupedbydate]

    # in the template, 
    # times are used to generate the table header and
    # dates are used to generate rows.
    # the radio options are not actually held in dates, 
    # rather, they are retreived from the form object according to the ticket ids in dates
    return render_template('event.html', event=event, bookform=bookform, times=times, dates=dates)



@events.route('/book', methods=['POST'])
@login_required
def book():
    form = BookEventForm()
    if form.validate_on_submit():
        # TODO: get the data from the form and validate it
        # TODO: use current_user and datetime.now()

        new_booking = Booking.book() # TODO: actually send the data along to create
        # TODO: use the response from book() to flash() something
        return redirect( url_for('main.bookings') )

    # TODO: flash() something here about how the form wasnt received
    return redirect( url_for('main.index') )



@events.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if not current_user.is_admin():
        flash( "You are not an administrator. You can't create events", 'danger' )
        return redirect( url_for('main.index') )

    form = CreateEventForm() 
    form.category.choices = Event.getAllCategories()

    if form.validate_on_submit():
        db_file_path = check_upload_file(form)
        
        if len(form.newcategory.data)==0:
            category = form.category.data
        else:
            category = form.newcategory.data
        
        name = form.name.data
        description = form.desc.data
        status = form.status.data
        image = db_file_path

        new_event = Event.create(name,description,category,status,image)

        tickets = json.loads(form.tickets.data)
        x = 0
        for ticket in tickets:
            x = x + 1

            Ticket.release(
                new_event.id, 
                ticket["datetime"], # TODO: this needs to be a datetime object from string w/ format: 2021-01-01 10:00
                ticket["numberOfGondolas"], 
                ticket["price"], 
                x
            )

        flash(f'Successfully created {form.name.data}', 'success')
        return redirect( url_for('events.event', id=new_event.id))

    return render_template('create.html', form=form)



def check_upload_file(form):
    # get file data from form
    fp = form.image.data
    filename = fp.filename
    # get the current path of the module file… store image file relative to this path
    BASE_PATH = os.path.dirname(__file__)
    #upload file location – directory of this file/static/image
    upload_path = os.path.join(BASE_PATH, 'static/images', secure_filename(filename))
    # store relative path in DB as image location in HTML is relative
    db_upload_path = '/static/images/'+ secure_filename(filename)
    # save the file and return the db upload path
    fp.save(upload_path)
    return db_upload_path



@events.route('/')
def viewAll():
    events = Event.getAll() # TODO: this method needs to be written
    form = SearchForm() # TODO: create this form

    # TODO: passing events to this template doesnt do anything
    # return render_template('events.html', events=events, form=form)
    return render_template('events.html')



@main.route('/bookings')
@login_required
def bookings():
    bookings = Booking.getAllByUser(current_user.id)

    # TODO: for convenience, pass a list of dictionaries to the template... like this but python    
    # bookings = bookings.map( booking => ({ 
    #     ...booking, 
    #     'ticket' : booking.getTicket(), 
    #     'event' : this.ticket.getEvent() 
    # }) )
    # return render_template('bookings.html', bookings=bookings)
    return render_template('bookings.html')



@main.route('/')
def index():
    upcoming = Event.getTopThreeByStatus('upcoming')
    cancelled = Event.getTopThreeByStatus('cancelled')
    form = indexForm()
    # return render_template('index.html', upcoming=upcoming, cancelled=cancelled)
    return render_template('index.html',form=form, upcoming=upcoming, cancelled=cancelled)