from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for
from flask.helpers import flash
from flask_login import current_user, login_required
from .forms import CreateEventForm, BookEventForm, SearchForm
from .models import Event, Booking


main = Blueprint('main', __name__)
events = Blueprint('events', __name__, url_prefix='/events')


@events.route('/<int:id>/update')
def update(id):
    form = CreateEventForm() # TODO: create this form
    event = Event.get(id)

    # TODO: passing a form to this template does nothing
    # TODO: passing an event to this template does nothing
    return render_template('create.html', form=form, event=event) 



@events.route('/<int:id>')
def view(id):
    form = BookEventForm() # TODO: create this form
    event = Event.get(id)

    # TODO: passing a form to this template does nothing
    # TODO: check how else the event object could be used in the template. it's started already
    return render_template('event.html', form=form, event=event)



@events.route('/book', methods=['POST'])
@login_required
def book():
    form = BookEventForm() # TODO: create this form
    if form.validate_on_submit():
        # TODO: see events.view first. It's not actually using this form yet
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

    form = CreateEventForm() # TODO: create this form
    if form.validate_on_submit():
        # TODO: get all of the data from the form
        new_event = Event.create() # TODO: actually send the data along to create
        # TODO: use the response from create() to flash() something
        return redirect( url_for('events.view', id=1) ) # TODO: actually send the new_event.id

    # TODO: passing a form to this template does nothing
    return render_template('create.html', form=form)



@events.route('/')
def viewAll():
    events = Event.getAll() # TODO: this method needs to be written
    form = SearchForm() # TODO: create this form

    # TODO: passing events to this template doesnt do anything
    return render_template('events.html', events=events, form=form) 



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
    return render_template('bookings.html', bookings=bookings)



@main.route('/')
def index():
    upcoming = Event.getAllByStatus('upcoming')
    cancelled = Event.getAllByStatus('cancelled')
    return render_template('index.html', upcoming=upcoming, cancelled=cancelled)