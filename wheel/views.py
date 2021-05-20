from flask import Blueprint, render_template
from .forms import CreateEventForm


main = Blueprint('main', __name__)
events = Blueprint('events', __name__, url_prefix='/events')

@events.route('/')
def viewAll():
    return render_template('events.html')

@main.route('/')
def index():
    return render_template('index.html')