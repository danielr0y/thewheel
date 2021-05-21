from flask import Blueprint, render_template, redirect, url_for
from flask.helpers import flash
from flask_login import current_user, login_required
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
@login_required
def book():
    form = BookEventForm()
    if form.validate_on_submit():
        # enter into database 
        return redirect( url_for('main.bookings') )

    return redirect( url_for('main.index') )



@events.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if not current_user.is_admin():
        flash( "You are not an administrator. You can't create events", 'danger' )
        return redirect( url_for('main.index') )

    form = CreateEventForm()
    if form.validate_on_submit():
        # enter into database 
        return redirect( url_for('events.view', id=1) )

    return render_template('create.html', form=form)



@events.route('/')
def viewAll():
    return render_template('events.html')



@main.route('/bookings')
@login_required
def bookings():
       
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