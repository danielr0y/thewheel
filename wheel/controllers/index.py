from flask import Blueprint, render_template

from wheel.models import Event
from wheel.forms import SearchForm

index = Blueprint('index', __name__)


@index.route('/')
def get():

    upcoming = Event.getAllByStatus('upcoming', 3)
    cancelled = Event.getAllByStatus('cancelled', 3)

    form = SearchForm() 
    form.category.choices = [("all", "all categories"), *[(category, category) for category in Event.getAllCategories()]]
    
    return render_template('index.html', upcoming=upcoming, cancelled=cancelled, form=form)