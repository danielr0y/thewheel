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



@events.route('/')
def viewAll():
    upcoming = Event.getAllByStatus("upcoming")
    booked = Event.getAllByStatus("booked out")
    cancelled = Event.getAllByStatus("cancelled")
    inactive = Event.getAllByStatus("inactive")

    form = SearchForm() # TODO: create this form

    # TODO: passing events to this template doesnt do anything
    # return render_template('events.html', events=events, form=form)
    return render_template('events.html', upcoming = upcoming, booked = booked, cancelled = cancelled, inactive = inactive )
    


@events.route('/<int:id>/update')
def update(id):
    form = CreateEventForm() # TODO: this form has now been created. use it.
    event = Event.get(id)
    form.name.data = event.name
    form.desc.data = event.description
    form.image.data = event.image
    form.status.data = event.status
    form.category.data = event.category
    #form.newcategory.data = event.newcategory


    # get rid of this and stop passing it
    bookform = BookEventForm()
    reviewform = PostReviewForm() 

    # TODO: pass the event to the create template
    # return render_template('create.html', form=form, event=event) 
    return render_template('update.html', form=form, event=event, bookform = bookform, reviewform = reviewform)
    

@events.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    
    event = Event.get(id)

    for x in event.tickets:

        delete_bookings =  Booking.query.filter_by(ticket_id=x.id).all()
        for y in delete_bookings:
            db.session.delete(y)
            db.session.commit()

        db.session.delete(x)
        db.session.commit()
        

    db.session.delete(event)
    db.session.commit()

    flash(f'Successfully deleted event', 'success')
    return redirect( url_for('events.viewAll') )




@events.route('/<int:id>')
def view(id):
    event = Event.get(id)
    bookform = BookEventForm()
    reviewform = PostReviewForm() 

    bookform.event.data = id
    # create radio field options from the tickets 
    bookform.ticket.choices = list(map(lambda ticket: (ticket.id, f'${ticket.price}'), event.tickets))

    # get a list of all possible times in order
    ticketssortedbytime = sorted(event.tickets, key=lambda ticket: ticket.datetime.strftime("%I:%M %p"))
    ticketsgroupedbytime = groupby(ticketssortedbytime, key=lambda ticket: ticket.datetime.strftime("%I:%M %p"))
    times = [time for time, _tickets in ticketsgroupedbytime]

    # get a list of ticket ids and the remaining tickets grouped by date
    ticketssortedbydate = sorted(event.tickets, key=lambda ticket: ticket.datetime)    
    ticketsgroupedbydate = groupby(ticketssortedbydate, key=lambda ticket: ticket.datetime.strftime("%d/%m/%Y"))
    dates = [[date, [[time.id, time.remaining] for time in times]] for date, times in ticketsgroupedbydate]

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
    current_event = Event.get(form.event.data)
    form.ticket.choices = list(map(lambda ticket: (ticket.id, f'${ticket.price}'), current_event.tickets))

    if form.validate_on_submit():    
        qty = form.qty.data
        total_price = form.price.data
        purchase_datetime = datetime.now()
        user_id = current_user.id
        ticket_id = form.ticket.data      

        error, remaining, booking_id = Booking.book(qty, total_price, purchase_datetime, user_id, ticket_id)

        if error:
            flash(f'Sorry, there are only {remaining} gondolas available for that time, please try again.', 'danger')
            return redirect( url_for('events.view', id=current_event.id)) 
        
        flash(f'Successfully booked {qty} tickets. Your booking ID is: {booking_id}', 'success')
        return redirect( url_for('main.bookings') )

    flash(f'Sorry, you cannot book an event with no availability.', 'danger')
    return redirect( url_for('main.index') )



@events.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if not current_user.is_admin():
        flash( "You are not an administrator. You can't create events", 'danger' )
        return redirect( url_for('main.index') )

    form = CreateEventForm() 
    form.category.choices = [("", "new category"), *[(category, category) for category in Event.getAllCategories()]]
    
    def changeDefaultStatus(status):
        form.status.default = status
        form.process()
        return form.status
    
    form.changeDefaultStatus = lambda status: changeDefaultStatus(status)

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
        jsonTickets = form.tickets.data

        new_event = Event.create(name,description,category,status,image)

        if jsonTickets:
            tickets = json.loads(jsonTickets)

            for ticket in tickets:
                datetimeobj = datetime.strptime(ticket["datetime"], '%Y-%m-%d %H:%M'),
                print(datetimeobj)

                Ticket.release(
                    new_event.id, 
                    datetimeobj,
                    ticket["numberOfGondolas"], 
                    ticket["price"]
                )

        flash(f'Successfully created {form.name.data}', 'success')
        return redirect( url_for('events.view', id=new_event.id))

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




@main.route('/bookings')
@login_required
def bookings():
    bookings = Booking.getAllByUser(current_user.id)
    
    dictionary = {}
    for booking in bookings:
        ticket = Ticket.query.get(booking.ticket_id)
        event = Event.query.get(ticket.event_id)
        dictionary[booking.id] = { 
            "Event ID: " : event.id, # have to have event ID in here for linking purposes
            "Order ID:": booking.id,
            "Event name: ": event.name,
            "Ticket date: ": ticket.datetime.strftime("%d/%m/%Y"),
            "Ticket time: ": ticket.datetime.strftime("%I:%M %p"),
            "Total price: ": booking.total_price,
            "Purchase date: ": booking.purchase_datetime.strftime("%d/%m/%Y %I:%M %p"),
            "Ticket quantity: ": booking.qty,
            "Event status: ": event.status,
        }
    
    print(dictionary.values())

    

    # TODO: for convenience, pass a list of dictionaries to the template... like this but python    
    # bookings = bookings.map( booking => ({ 
    #     ...booking, 
    #     'ticket' : booking.getTicket(), 
    #     'event' : this.ticket.getEvent() 
    # }) )
    # return render_template('bookings.html', bookings=bookings)
    return render_template('bookings.html', bookings = dictionary)



@main.route('/')
def index():
    upcoming = Event.getTopThreeByStatus('upcoming')
    cancelled = Event.getTopThreeByStatus('cancelled')
    form = indexForm()
    # return render_template('index.html', upcoming=upcoming, cancelled=cancelled)
    return render_template('index.html',form=form, upcoming=upcoming, cancelled=cancelled)