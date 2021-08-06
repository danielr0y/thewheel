# Python web application with Flask
[https://iab207thewheel.herokuapp.com/](https://iab207thewheel.herokuapp.com/)

## Summary
This conventional web application project uses the Python web framework Flask and its associated templating, session management and database connectivity libraries to serve a simple event management website styled with Bootstrap.

### Technologies
* Python
* Flask
* SQLAlchemy object-relational mapper and query builder
* SQLite
* WTForms server-side input validation
* HTML
* Bootstrap 5
* JavaScript event-driven DOM manipulation
* Client-side form validation with JS

## Architecture 
This project follows an MVC architecture and uses SQLAlchemy to map in-memory data models with an SQLite database.\
URL routes are associated with controller functions using Flask `route()` decorators, those functions instruct  Python data model classes/objects to perform CRUD operations on their mapped relational models and those now updated in-memory models are passed onto the views to create a response.

## Brief
From romantic dining experiences to front-row seats to our nation’s best fireworks displays, The Wheel of Brisbane frequently hosts special events offering a unique perspective of our beautiful city to visitors and locals alike. This project aims to aid The Wheel of Brisbane in improving online ticket sales for such events by leveraging the good word of their many satisfied customers and by providing a modern, user-friendly event management system tailored to their specific needs. With the potential to service up to 252 guests in 42 gondolas twice an hour and the need to continue accommodating ticket sales at the gate, any credible solution will require a sophisticated approach to modelling events, tickets, bookings and their numerous relationships. Some of the unique requirements of this event management system include:
* Events that span multiple days or weeks
* Events that occur at several times on one date
* Variable number of gondolas for each date/time slot (herein ‘ticket’) e.g.) Weekend dining events may only reserve 12 gondolas where fireworks events will reserve 42.
* Variable number of passengers permissible in one gondola (max 6) and
* Variable rates for different tickets to the same event

## Design
User stories, conceptual- and data models and wireframe designs can be found in the design document at [https://github.com/danielr0y/thewheel/n8031789_design_rwad.pdf](https://github.com/danielr0y/thewheel/blob/45a80215a0084b3e77a62b7e029c86b147d9d5ec/n8031789_design_rwad.pdf)

## User Guide
### Administrator account
email: admin@thewheel.com.au\
passw: admin\
Please feel free to create some events. They will only persist until the dyno sleeps again.

Administrators can create, update and delete events, release tickets for events and change the status of events.\
Guests can register for a customer account then book tickets for an event, see their previous bookings and leave comments on events.

Each time a booking is made, the number of gondolas for that ticket/time-slot is reduced according to the number of tickets sold until there are no more tickets available. That time-slot then becomes unavailable. Once all time-slots for an event are unavailable, the event becomes booked out.\
Once all tickets for an event are in the past, the event will become inactive and will no longer be shown to customers. Administrators can still update these events to release more tickets for the future.
