from flask import Blueprint, render_template


main = Blueprint('main', __name__)
events = Blueprint('events', __name__, url_prefix='/events')

@events.route('/create')
def create():
    return render_template('create.html')

@events.route('/')
def viewAll():
    return render_template('events.html')

@main.route('/')
def index():
    return render_template('index.html')