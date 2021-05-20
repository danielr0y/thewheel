from flask import Blueprint, render_template
from .models import Event


main = Blueprint('main', __name__)
events = Blueprint('events', __name__, url_prefix='/events')

@events.route('/create')
def create():
@events.route('/<int:id>')
def view(id):
    event = Event.query.filter_by(id=id).first()

    return render_template('event.html', event=event)



@events.route('/')
def viewAll():
    return render_template('events.html')

@main.route('/')
def index():
    return render_template('index.html')