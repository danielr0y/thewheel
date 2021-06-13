from datetime import datetime

from flask import Blueprint, render_template
from flask_login import current_user, login_required

from wheel.models import Booking

bookings = Blueprint('bookings', __name__, url_prefix='/bookings')


@bookings.route('/<int:id>')
@bookings.route('/')
@login_required
def get(id=None):
    if id:
        booking = Booking.get(id)
        ticket = booking.getTicket()
        event = booking.getEvent()

    bookings = [[booking, ticket, event]] if id else \
        [[booking, booking.getTicket(), booking.getEvent()] for booking in Booking.getAllByUser(current_user.id)]

    return render_template('bookings.html', bookings=bookings, now=datetime.now() )