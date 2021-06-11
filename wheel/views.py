from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request
from flask.helpers import flash
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os, json
from .forms import CreateEventForm, BookEventForm, SearchForm, PostReviewForm
from .models import Event, Booking, Ticket, Review
from . import db 


main = Blueprint('main', __name__)
events = Blueprint('events', __name__, url_prefix='/events')




@events.route('/')

def viewAll():

    search =  request.args['search']

    categories = Event.getAllCategories()

    if search == None:

        events = Event.getAll()

    elif search in categories:

        events = Event.getAllByCategory(search)

    else:

        events = Event.getAllBySearch(search)

    
    return render_template('events.html', events=events, categories=categories)


@events.route('/<int:id>/review', methods=['POST'])
@login_required
def reviewCreate(id):
    form = PostReviewForm() 
    event = Event.query.get(id)
    if form.validate_on_submit(): 

        Review.post(event.id, current_user.id, form.text.data)
        flash('Review Created!', 'success')
        
    else:
        flash('Issue posting review', 'danger')

    return redirect( url_for('events.view', id=id))

@events.route('/<int:id>')
def view(id):
    event = Event.get(id)
    tickets = event.getFutureTickets()

    if len(tickets) == 0:
        if event.status != 'cancelled':
            event.updateStatus("inactive")
        
    times = Ticket.getAllTimesFromTickets(tickets)
    dates = Ticket.groupTicketsByDate(tickets)

        

    bookform = BookEventForm()
    reviewform = PostReviewForm() # TODO: create this form

    # TODO: validate the review form here
    # don't put database logic here
    # USE Review.post() it's already written for you

    #Review.post(event_id, author_id, text)

    # set default values
    bookform.ticket.choices = list(map( lambda ticket: (ticket.id, f'${ticket.price}'), tickets ))

    # in the template, 
    # times are used to generate the table header and
    # dates are used to generate rows.
    # the radio options are not actually held in dates, 
    # rather, they are retreived from the form object according to the ticket ids in dates
    return render_template('event.html', event=event, bookform=bookform, times=times, dates=dates, rform=reviewform)


@events.route('/<int:id>/update', methods=['GET', 'POST'])
@events.route('/create', methods=['GET', 'POST'])
@login_required
def create(id=None):
    if not current_user.is_admin():
        flash( "You are not an administrator. You can't create events", 'danger' )
        return redirect( url_for('main.index') )

    form = CreateEventForm() 
    form.category.choices = [("", "new category"), *[(category, category) for category in Event.getAllCategories()]]

    if form.validate_on_submit(): 
        # POST goes this way
        existing_event = Event.get(id) if id else False
        
        name = form.name.data
        description = form.desc.data
        existing_category = form.category.data
        category = existing_category if existing_category else form.newcategory.data
        status = form.status.data
        image = check_upload_file(form.image.data)
        jsonTickets = form.tickets.data

        event = existing_event.set(name, description, category, status, image) if existing_event else \
                Event.create(name, description, category, status, image)

        if jsonTickets:
            tickets = json.loads(jsonTickets)

            if existing_event: 
                event.deleteAllTickets()

            for ticket in tickets:
                datetimeobj = datetime.strptime(ticket["datetime"], '%Y-%m-%d %H:%M'),
                Ticket.release( event.id, datetimeobj, ticket["numberOfGondolas"], ticket["price"] )

        flash(f'Successfully created {form.name.data}', 'success')
        return redirect( url_for('events.view', id=event.id))

    # GET goes this way 
    form.changeDefaultStatus = lambda status: changeDefaultStatus(status)
    def changeDefaultStatus(status):
        form.status.default = status
        form.process()
        return form.status

    if id:
        # UPDATE
        event = Event.get(id)
        tickets = [ { 
            "date": date, 
            "tickets": [ {
                "remaining": ticket.remaining, 
                "price": ticket.price
            } for ticket in tickets]
        } for date, tickets in Ticket.groupTicketsByDate(event.tickets) ]

        form.name.data = event.name
        form.desc.data = event.description
        form.image.data = event.image
        form.status.data = event.status
        form.category.data = event.category
        form.newcategory.data = event.category

        return render_template('create.html', form=form, event_id=id, tickets=json.dumps(tickets) )
    
    # CREATE
    return render_template('create.html', form=form, event_id=id)



def check_upload_file(image):
    if not image:
        return None
        
    filename = image.filename
    # get the current path of the module file… store image file relative to this path
    BASE_PATH = os.path.dirname(__file__)
    #upload file location – directory of this file/static/image
    upload_path = os.path.join(BASE_PATH, 'static/images', secure_filename(filename))
    # store relative path in DB as image location in HTML is relative
    db_upload_path = '/static/images/'+ secure_filename(filename)
    # save the file and return the db upload path
    image.save(upload_path)
    return db_upload_path
    


    

@events.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    event = Event.get(id)
    event.delete()

    flash(f'Successfully deleted event', 'success')
    return redirect( url_for('events.viewAll') )



@events.route('/<int:id>/book', methods=['POST'])
@login_required
def book(id):
    form = BookEventForm()
    event = Event.get(id)
    form.ticket.choices = list(map(lambda ticket: (ticket.id, f'${ticket.price}'), event.getFutureTickets()))

    if form.validate_on_submit():    
        qty = form.qty.data
        total_price = form.price.data
        purchase_datetime = datetime.now()
        user_id = current_user.id
        ticket_id = form.ticket.data      

        error, remaining, booking_id = Booking.book(qty, total_price, purchase_datetime, user_id, ticket_id)

        if error:
            flash(f'Sorry, there are only {remaining} gondolas available for that time, please try again.', 'danger')
            return redirect( url_for('events.view', id=event.id)) 
        
        flash(f'Successfully booked {qty} tickets. Your booking ID is: {booking_id}', 'success')
        return redirect( url_for('main.bookings') )

    flash(f'Sorry, you cannot book an event with no availability.', 'danger')
    return redirect( url_for('main.index') )




@main.route('/bookings')
@login_required
def bookings():
    bookings = [ [
            booking, 
            booking.getTicket(), 
            booking.getEvent()
    ] for booking in Booking.getAllByUser(current_user.id)]
    
    return render_template('bookings.html', bookings = bookings)



@main.route('/')
def index():
    upcoming = Event.getAllByStatus('upcoming', 3)
    cancelled = Event.getAllByStatus('cancelled', 3)

    form = SearchForm() 
    form.search.choices = [*[(category, category) for category in Event.getAllCategories()]]

    

    
    return render_template('index.html', upcoming=upcoming, cancelled=cancelled, form = form)