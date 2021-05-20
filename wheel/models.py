from . import db
from flask_login import UserMixin
from datetime import datetime


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
    def get(email):
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
    def get(id):
        return Event.query.filter_by(id=id).first()

    def ticketsDateRange(self):
        return {
            "on": datetime.now().date().strftime("%d/%m/%Y"),
            "and": datetime.now().date().strftime("%d/%m/%Y")
        }

    def ticketsTimeRange(self):
        return {
            "from": datetime.now().strftime("%I:%M %p"), # self.tickets.reduce( (prev, {datetime}) => lowest(prev, datetime) ) but python
            "until": datetime.now().strftime("%I:%M %p") # self.tickets.reduce( (prev, {datetime}) => highest(prev, datetime) ) but python
        }

    def ticketsFromPrice(self):
        return 100 # self.tickets.reduce( (prev, {price}) => lowest(prev, price) ) but python

    def statusColour(self):
        return {
            'upcoming': 'success',
            'inactive': 'secondary',
            'booked out': 'secondary',
            'cancelled': 'danger'
        }[self.status]

    def bookButtonText(self):
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



class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    remaining = db.Column(db.Integer, nullable=False)

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    @staticmethod
    def get(id):
        return Ticket.query.filter_by(id=id).first()

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

    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'))

    def getTicket(self):
        return Ticket.get(self.ticket_id)