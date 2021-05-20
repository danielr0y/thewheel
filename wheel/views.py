from flask import Blueprint, render_template
from .forms import CreateEventForm
from .models import Event


main = Blueprint('main', __name__)
events = Blueprint('events', __name__, url_prefix='/events')

@events.route('/create', methods=['GET', 'POST'])
def create():
    form = CreateEventForm()
    # if submitted
        # enter into database 
        # redirect new event
    return render_template('create.html', form=form)



@events.route('/<int:id>/update')
def update(id):
    form = CreateEventForm()
    event = Event.query.filter_by(id=id).first()

    return render_template('create.html', form=form, event=event)



@events.route('/<int:id>')
def view(id):
    event = Event.query.filter_by(id=id).first()

    return render_template('event.html', event=event)



@events.route('/')
def viewAll():
    return render_template('events.html')



@main.route('/')
def index():
    # upcoming = get from database
    # cancelled = get from database
    # return render_template('index.html', upcoming=upcoming, cancelled=cancelled)
    return render_template('index.html')