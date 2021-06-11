from itertools import groupby
from functools import reduce
from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum('customer','administrator'), nullable=False, default='customer')

    reviews = db.relationship('Review', backref='author')
    bookings = db.relationship('Booking', backref='customer')


    @staticmethod
    def register(name, email, password):
        if User.getByEmail(email):
            return False

        pwd_hash = generate_password_hash(password)
        new_user = User(name=name, password_hash=pwd_hash, email=email)

        db.session.add(new_user)
        db.session.commit()

        return True


    @staticmethod
    def login(email, password):
        user = User.getByEmail(email)

        if user is None:
            return [False, 'Incorrect email']
        
        if not check_password_hash(user.password_hash, password):
            return [False, 'Incorrect password']

        login_user(user)
        return [True, 'Welcome back'] 


    @staticmethod
    def get(id: int):
        return User.query.get(id)


    @staticmethod
    def getByEmail(email):
        return User.query.filter_by(email=email).first()


    def is_admin(self):
        return self.type == 'administrator'



class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(40))
    status = db.Column(db.Enum('upcoming', 'inactive', 'cancelled', 'booked out'), nullable=False)
    image = db.Column(db.String(255))

    reviews = db.relationship('Review', backref='event')
    tickets = db.relationship('Ticket', backref='event')


    @staticmethod
    def create(name, description, category, status, image):
        event = Event(name=name, description=description, category=category, status=status, image=image)
        
        db.session.add(event)
        db.session.commit()
       
        return event


    @staticmethod
    def get(id: int):
        return Event.query.get(id)


    def updateStatusInactive(self):
        # FIXME: I don't think this is working properly.
        x_max = datetime(2000,9,9)

        for x in self.tickets:
            if x.datetime > x_max:
                x_max = x.datetime

        if x_max < datetime.now():

            self.status = 'inactive'
            db.session.commit()
            return

        elif self.status == 'inactive':

            self.status = 'upcoming'
            db.session.commit()
            return
        
        return


    @staticmethod
    def getAll():
        # gets events with tickets in the future
        return Event.query.\
            join(Ticket).\
            filter( Ticket.datetime > datetime.now() ).\
            group_by( Event.id ).\
            order_by( Ticket.datetime ).\
            all()


    @staticmethod
    def getAllByStatus(status, limit=None):
        # gets events with tickets in the future by status
        return Event.query.\
            join( Ticket ).\
            filter( Ticket.datetime > datetime.now() ).\
            filter( Event.status == status ).\
            group_by( Event.id ).\
            order_by( Ticket.datetime ).\
            limit( limit ).\
            all()


    @staticmethod
    def getAllByCategory(category):
        # gets events with tickets in the future by category
        return Event.query.\
            join( Ticket ).\
            filter( Ticket.datetime > datetime.now() ).\
            filter( Event.category == category ).\
            group_by( Event.id ).\
            order_by( Ticket.datetime ).\
            all()


    @staticmethod
    def getAllCategories():
        return [event.category for event in Event.query.group_by('category').all()]


    def set(self, name, description, category, status, image):
        self.name = name
        self.description = description
        self.category = category
        self.status = status

        if image:
            self.image = image

        db.session.commit()
        return self


    def delete(self):
        self.deleteAllTickets()
        self.deleteAllReviews()

        db.session.delete(self)
        db.session.commit()


    def deleteAllTickets(self):
        for ticket in self.tickets:
            ticket.delete()


    def deleteAllReviews(self):
        for review in self.reviews:
            review.delete()



    def getFutureTickets(self):
        return list( filter( lambda ticket: ticket.datetime > datetime.now(), self.tickets ) )


    def getAllTicketTimes(self):
        # returns a list of time strings for this event 
        tickets = self.getFutureTickets()

        ticketssortedbytime = sorted(tickets, key=lambda ticket: ticket.datetime.strftime("%I:%M %p"))
        ticketsgroupedbytime = groupby(ticketssortedbytime, key=lambda ticket: ticket.datetime.strftime("%I:%M %p"))
        
        # return lists instead of itertool objects
        return [time for time, tickets in ticketsgroupedbytime]


    def getAllTicketsGroupedByDate(self):
        # returns all of the future tickets for this event grouped by date
        tickets = self.getFutureTickets()

        ticketssortedbydate = sorted(tickets, key=lambda ticket: ticket.datetime)    
        ticketsgroupedbydate = groupby(ticketssortedbydate, key=lambda ticket: ticket.datetime.strftime("%d/%m/%Y"))
        
        # return lists instead of itertool objects
        return [[date, [time for time in times]] for date, times in ticketsgroupedbydate]


    def getTicketsRange(self):
        tickets = self.getFutureTickets()
        numberOfTickets = len(tickets)

        if numberOfTickets == 0:
            return [numberOfTickets, None, None]

        min_ticket = reduce( lambda x, y: min(x, y, key=lambda ticket: ticket.datetime), tickets )
        max_ticket = reduce( lambda x, y: max(x, y, key=lambda ticket: ticket.datetime), tickets )
        
        return [numberOfTickets, min_ticket, max_ticket]


    def printTicketsDateRange(self):
        numberOftickets, min_ticket, max_ticket = self.getTicketsRange()

        if numberOftickets == 0:
            return "There are no tickets for this event."

        min = min_ticket.datetime.strftime("%d/%m/%Y")
        max = max_ticket.datetime.strftime("%d/%m/%Y")

        if min == max:
            return f"on: {min}"
            
        return f"from: {min} until: {max}"


    def printTicketsTimeRange(self):
        numberOftickets, min_ticket, max_ticket = self.getTicketsRange()

        if numberOftickets == 0:
            return "There are no tickets for this event."

        min = min_ticket.datetime.strftime("%I:%M%p")
        max = max_ticket.datetime.strftime("%I:%M%p")

        if numberOftickets == 1:
            return f"at: {min}"

        if numberOftickets == 2:
            return f"at: {min} and: {max}"
            
        return f"from: {min} until: {max}"


    def getTicketsPriceFrom(self):
        low_ticket = 100000

        for x in self.tickets:
            if x.price < low_ticket:
                low_ticket = x.price
        
        if low_ticket == 100000:
            return " "

        low = str(low_ticket)

        return "from $" + low
        

    def getStatusColour(self):
        return {
            'upcoming': 'success',
            'inactive': 'secondary',
            'booked out': 'secondary',
            'cancelled': 'danger'
        }[self.status]


    def getBookButtonText(self):
        return {
            'upcoming': 'book now',
            'inactive': 'no tickets available',
            'booked out': 'booked out',
            'cancelled': 'cancelled'
        }[self.status]



class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    time = db.Column(db.DateTime, default=datetime.now())

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))


    @staticmethod
    def getAllByEvent(event_id):
        return 


    @staticmethod
    def post(event_id, author_id, text):
        time = datetime.now()
        review = Review( event_id=event_id, author_id=author_id, time=time, text=text )

        db.session.add(review)
        db.session.commit()
        return 


    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return 



class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    remaining = db.Column(db.Integer, nullable=False)

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))


    @staticmethod
    def release(event_id, datetime, numberOfGondolas, ticketprice):
        ticket = Ticket(event_id = event_id, datetime = datetime[0], remaining = numberOfGondolas, price = ticketprice)

        db.session.add(ticket)
        db.session.commit()
        
        return ticket


    @staticmethod
    def get(id: int):
        return Ticket.query.get(id)


    def delete(self):
        Booking.deleteAllByTicket(self.id)

        db.session.delete(self)
        db.session.commit()

    
    def getEvent(self):
        return Event.get(self.event_id)


    def getDate(self):
        return self.datetime.date()


    def getTime(self):
        return self.datetime.time()



class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False) 
    purchase_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'))


    @staticmethod
    def get(id: int):
        return Booking.query.get(id)


    @staticmethod
    def getEventID(booking_id):
        booking = Booking.query.get(booking_id)
        ticket = Ticket.query.get(booking.ticket_id)
        event = Event.query.get(ticket.event_id)
        return event.id


    @staticmethod
    def getAllByUser(user_id):
        return Booking.query.filter_by(user_id=user_id)


    @staticmethod
    def deleteAllByTicket(ticket_id):
        bookings = Booking.query.filter_by(ticket_id=ticket_id).all()
        
        for booking in bookings:
            booking.delete()


    @staticmethod
    def book(qty, price, datetime, user, ticket_id):
        ticket = Ticket.get(ticket_id)
        remaining = ticket.remaining

        # deal with errors first
        if qty > remaining:
            return [True, remaining, None] # error, number of gondolas remaining, booking_id

        # otherwise, make the booking
        booking = Booking(qty = qty , total_price = price , purchase_datetime = datetime , user_id = user , ticket_id = ticket_id)
        ticket.remaining = remaining - qty

        # if that was the last ticket, check if the event status needs to be updated
        if qty == remaining: 
            event = Event.get(ticket.event_id)

            otherRemainingTickets = list(filter(lambda ticket: ticket.remaining > 0, event.tickets))
            if not len(otherRemainingTickets):
                event.status = "booked out"
    
        # add and commit changes
        db.session.add(booking)
        db.session.commit() 

        return [False, remaining, booking.id]


    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def getUser(self):
        return User.get(self.user_id)


    def getTicket(self):
        return Ticket.get(self.ticket_id)