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
            return 'Incorrect email'
        
        if not check_password_hash(user.password_hash, password):
            return 'Incorrect password'

        login_user(user)
        return False # returns errors, so False means success


    @staticmethod
    def get(id):
        return User.query.filter_by(id=id).first()


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
    def get(id):
        return Event.query.filter_by(id=id).first()


    @staticmethod
    def getAll():
        # TODO: 
        return 


    @staticmethod
    def getAllByStatus(status):
        # TODO:
        return 


    @staticmethod
    def getAllByCategory(category):
        # TODO:
        return 


    @staticmethod
    def getAllCategories():
        return 


    def set(self, name, description, category, status, image):
        return 


    def getTicketsDateRange(self):
        return Ticket.getDateRangeByEvent(self.id)


    def getTicketsTimeRange(self):
        return Ticket.getTimeRangeByEvent(self.id)


    def getTicketsPriceFrom(self):
        return 100 # self.tickets.reduce( (prev, {price}) => lowest(prev, price) ) but python


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
        return 



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


    @staticmethod
    def getTimeRangeByEvent(event_id):
        return {
            "from": datetime.now().strftime("%I:%M %p"), # self.tickets.reduce( (prev, {datetime}) => lowest(prev, datetime) ) but python
            "until": datetime.now().strftime("%I:%M %p") # self.tickets.reduce( (prev, {datetime}) => highest(prev, datetime) ) but python
        }


    @staticmethod
    def getDateRangeByEvent(event_id):
        return {
            "on": datetime.now().date().strftime("%d/%m/%Y"),
            "and": datetime.now().date().strftime("%d/%m/%Y")
        }


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
    def get(id):
        return Booking.query.filter_by(id=id).first()


    @staticmethod
    def getAllByUser(user_id):
        return Booking.query.filter_by(user_id=user_id)


    @staticmethod
    def book(): # TODO: what args does this need?
        # TODO: use Booking() constructor
        # TODO: check that a booking was created and return errors if neccessary
        return


    def getUser(self):
        return User.get(self.user_id)


    def getTicket(self):
        return Ticket.get(self.ticket_id)