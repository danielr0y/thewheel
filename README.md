# assignment3
IAB207 Assignment 3

My design document from assignment 1 is also included in the repo for your reference

administrator account
email: admin@thewheel.com 
passw: admin

I have used and recommend installing: TODO Highlight
https://marketplace.visualstudio.com/items?itemName=wayou.vscode-todo-highlight



Next steps:
we could do all the simple views that get things from the database but then we would have to manually add a bunch of stuff into the database so I think we should start with create event.

I have started building out the structure for the create event page.
there is a view @events.create which suggests we use the CreateEventForm
CreateEventForm does not exist yet so we'll need that first.
follow the pracs. should be pretty much the same as create destination. You can ignore tickets for now.

Then we'll need to use those form fields in the template.
we cant use quickform any more like we did in the pracs because we need more control over the HTML
this is a great resource https://wtforms.readthedocs.io/en/2.3.x/fields/
but you can also use event.html as a guide because I have already implemented that form and used form fields individually without quickform there.

When displaying the form, ie GET, we'll will need to retrieve the list of existing categories from the database and use them as the options for the select field. 
I have created Event.getAllCategories() but it doesnt do anything yet. 
and I have put notes in the view code about how to add those categories to the select field.

Regarding POST, 
I don't recall how image processing works but I've dumped the method check_upload_file() from the pracs in there already. use that.

use Event.create() which isn't actually implmented yet either.

the form should already come to the server with tickets included. I implemented it in JavaScript.
If they are not in the form they should be in the request object 
https://flask.palletsprojects.com/en/1.1.x/quickstart/#http-methods

these tickets are a JSON object. I don't know how python deals with JSON but I'm sure it won't be difficult. We'll need to loop through those objects and create tickets for each. 
use Tickets.release() passing the new_event.ID 
this method is also not implemented yet but it will pretty much just pass tickets on the the constructor, check that everything was successful and return the tickets or an error.



#1	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/views.py#18
	TODO: create this form

#2	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/views.py#21
	TODO: passing a form to this template does nothing

#3	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/views.py#22
	TODO: passing an event to this template does nothing

#4	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/views.py#32
	TODO: create this form

#5	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/views.py#61
	TODO: get the data from the form and validate it

#6	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/views.py#62
	TODO: use current_user and datetime.now()

#7	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/views.py#64
	TODO: actually send the data along to create

#8	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/views.py#65
	TODO: use the response from book() to flash() something

#9	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/views.py#68
	TODO: flash() something here about how the form wasnt received

#10	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/views.py#80
	TODO: create this form

#11	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/views.py#82
	TODO: get all of the data from the form

#12	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/views.py#84
	TODO: this is not complete. its just a guide. actually send the data along to create. 

#13	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/views.py#86
	TODO: process the tickets JSON object, loop through it creating tickets for each passing new_event.ID

#14	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/views.py#89
	TODO: use the response from create() to flash() something

#15	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/views.py#90
	TODO: actually send the new_event.id

#16	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/views.py#92
	TODO: if GET, populate the categories select field with choices

#17	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/views.py#97
	TODO: passing a form to this template does nothing

#18	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/views.py#119
	TODO: this method needs to be written

#19	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/views.py#120
	TODO: create this form

#20	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/views.py#122
	TODO: passing events to this template doesnt do anything

#21	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/views.py#133
	TODO: for convenience, pass a list of dictionaries to the template... like this but python    

#22	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/templates/create.html#7
	TODO:   use the form passed to this template

#23	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/templates/create.html#11
	TODO: (much later) use the event passed to this template to prefill the form with data when editing

#24	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/templates/event.html#9
	TODO: this page uses the event object a bit but it's not complete -->

#25	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/templates/event.html#21
	TODO: We're storing HTML in the database. How do we made Flask parse HTML? -->

#26	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/templates/events.html#3
	TODO: use the events passed to this template  -->

#27	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/templates/events.html#4
	TODO: search form?  -->

#28	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/templates/events.html#59
	TODO: {% for event in events %} -->

#29	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/forms.py#19
	TODO: add all the neccessary fields

#30	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/forms.py#20
	TODO: once this form is created we need to use the fields in template. Follow event.html as guide

#31	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/forms.py#32
	TODO: add all the neccessary fields

#32	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/forms.py#37
	TODO: add all the neccessary fields

#33	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/models.py#78
	TODO: implement this method. take arguements and pass them along to the constructor.

#34	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/models.py#90
	TODO: 

#35	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/models.py#96
	TODO:

#36	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/models.py#102
	TODO:

#37	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/models.py#108
	TODO: SELECT category FROM events GROUP BY category but with SQLAlchemy syntax

#38	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/models.py#180
	TODO: this method should take params for creating a new ticket and pass them onto the constructor

#39	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/models.py#181
	TODO: check that they were created successfully and return the tickets or an error.

#40	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/models.py#241
	TODO: what args does this need? all the properties?

#41	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/models.py#242
	TODO: use Booking() constructor. follow the tutorial about creating destinations

#42	file:///Users/daniel/Documents/Daniel/uni/2021SEM1/IAB207/assignment%203/assignment3/wheel/models.py#243
	TODO: check that a booking was created and return errors if neccessary