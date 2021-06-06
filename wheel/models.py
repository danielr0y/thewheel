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


    @staticmethod
    def getAll():
        # TODO: 
        return 


    def getAllByStatus(status):
        # TODO:
        return Event.query.filter_by(status=status).all()


    def getTopThreeByStatus(status):
        # TODO: maybe we should try and order by Ticket dates?
        return Event.query.filter_by(status=status).limit(3).all()



    @staticmethod
    def getAllByCategory(category):
        # TODO:
        return Event.query.filter_by(category=category).all()


    @staticmethod
    def getAllCategories():
        
        return [(Event.category) for Event in Event.query.group_by('category')]
        # TODO: SELECT category FROM events GROUP BY category but with SQLAlchemy syntax
        return 


    def set(self, name, description, category, status, image):
        return 


    def getTicketsDateRange(self):

        x_min = datetime(3000,9,9)
        x_max = datetime(2000,9,9)

        for x in self.tickets:
            if x.datetime < x_min:
                x_min = x.datetime

            if x.datetime > x_max:
                x_max = x.datetime
        
        low_date = x_min.strftime("%m/%d/%Y")
        low_time = x_min.strftime("%I:%M%p")

        high_date = x_max.strftime("%m/%d/%Y")
        high_time = x_max.strftime("%I:%M%p")

        output = "from " + low_time + " on " + low_date + ",  to " + high_time + " on " + high_date
             
        return output
        

    def getTicketsPriceFrom(self):
        
        low_ticket = 100000

        for x in self.tickets:
            if x.price < low_ticket:
                low_ticket = x.price
             
        return low_ticket

    def getTicketsStartDate(self):
        return Ticket.getStartDateByEvent(self.id)

    def getTicketsEndDate(self):
        return Ticket.getEndDateByEvent(self.id)


    def getTicketsTimeRange(self):
        return Ticket.getTimeRangeByEvent(self.id)

    def getTicketsStartTime(self):
        return Ticket.getStartTimeByEvent(self.id)

    def getTicketsEndTime(self):
        return Ticket.getEndTimeByEvent(self.id)
        


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
    def release(event_id, datetime, numberOfGondolas, ticketprice):
        ticket = Ticket(event_id = event_id, datetime = datetime[0], remaining = numberOfGondolas, price = ticketprice)

        db.session.add(ticket)
        db.session.commit()

        
        return ticket


    @staticmethod
    def get(id: int):
        return Ticket.query.get(id)

    
    @staticmethod
    def getTimeRangeByEvent(event_id):
         return {
            "from": datetime.now().strftime("%I:%M %p"), # self.tickets.reduce( (prev, {datetime}) => lowest(prev, datetime) ) but python
            "until": datetime.now().strftime("%I:%M %p") # self.tickets.reduce( (prev, {datetime}) => highest(prev, datetime) ) but python
        }


    @staticmethod
    def getStartTimeByEvent(event_id):
        return datetime.now().strftime("%I:%M %p") #Only returning a single time not pulling from db strftime again formats 

    @staticmethod
    def getEndTimeByEvent(event_id):
        return datetime.now().strftime("%I:%M %p") #Only returning a single time not pulling from db strftime again formats 

    def getStartDateByEvent(event_id):
        return  datetime.now().date().strftime("%d/%m/%Y") #Only returning a single date not pulling from db strftime formats weird on page

    def getEndDateByEvent(event_id):
        return  datetime.now().date().strftime("%d/%m/%Y") #Only returning a single date not pulling from db strftime formats weird on page


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
    def getAllByUser(user_id):
        return Booking.query.filter_by(user_id=user_id)


    @staticmethod
    def book(qty,price,datetime,user,ticket):
        
        ticket_temp = Ticket.get(ticket)

        outcome = 0

        if qty < ticket_temp.remaining:
            
            booking = Booking(qty = qty , total_price = price , purchase_datetime = datetime , user_id = user , ticket_id = ticket)
        
            db.session.add(booking)
            db.session.commit()

            ticket_temp.remaining = ticket_temp.remaining - qty
            db.session.commit()

            return outcome

        outcome = ticket_temp.remaining
        return outcome

        




    def getUser(self):
        return User.get(self.user_id)


    def getTicket(self):
        return Ticket.get(self.ticket_id)