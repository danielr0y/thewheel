from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from .forms import CreateEventForm, BookEventForm
from .models import Event


main = Blueprint('main', __name__)
events = Blueprint('events', __name__, url_prefix='/events')


@events.route('/<int:id>/update')
def update(id):
    form = CreateEventForm()
    event = Event.get(id)

    return render_template('create.html', form=form, event=event)



@events.route('/<int:id>')
def view(id):
    form = BookEventForm()
    event = Event.get(id)

    return render_template('event.html', form=form, event=event)



@events.route('/book', methods=['POST'])
def book():
    form = BookEventForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        # enter into database 
        return redirect( url_for('main.bookings') )

    return redirect( url_for('main.index') )



@events.route('/create', methods=['GET', 'POST'])
def create():
    form = CreateEventForm()
    if form.validate_on_submit() and current_user.is_authenticated and current_user.is_admin():
        # enter into database 
        return redirect( url_for('events.view', id=1) )

    return render_template('create.html', form=form)



@events.route('/')
def viewAll():
    return render_template('events.html')



@main.route('/bookings')
def bookings():
    if not current_user.is_authenticated:
        return redirect( url_for('main.index') )
        
    # bookings = current_user.bookings.map( booking => ({ 
    #     ...booking, 
    #     'ticket' : booking.getTicket(), 
    #     'event' : this.ticket.getEvent() 
    # }) )

    # return render_template('bookings.html', bookings=bookings)
    return render_template('bookings.html')



@main.route('/')
def index():
    # upcoming = get from database
    # cancelled = get from database
    # return render_template('index.html', upcoming=upcoming, cancelled=cancelled)
    return render_template('index.html')