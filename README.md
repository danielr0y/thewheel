# 8:Wed_5-7_Jason 2
Daniel Roy n8031789
Harvey Goldsmith n10534261
Matt Gill n10446435
Max Pyle n10765239

IAB207 Assignment 3

Administrator account
email: admin@thewheel.com.au
passw: admin

To create more admin accounts, create an account then log in with any existing admin account, click the accounts tab and select “make admin”.

a customer account with some edge case bookings. including bookings for events which were cancelled, booked out and which are now inactive
email: daniel@email.com 
passw: daniel

As outlined in the design document for assignment 1 (included in the repo), our project does not directly have dates associated with events. Instead, each event has many tickets. This allows an event to occur many times per day and over many days .

It is important to note that each individual ticket/time-slot has it's own number remaining. 
This number is shown when booking a ticket. If you try to book too many it will reject the booking.
A ticket is no longer available after this number reaches 0 but the event itself may not yet be "booked out". Only once all tickets/timeslots have no number remaining does the event then change to "booked out".

Once all tickets for an event are in the past, the event will become "inactive". Inactive events can only be found via the My Bookings page or by inserting the ID in the URL. for example,
https://iab207thewheel.herokuapp.com/events/15

An administrator can update an inactive event from last year (Valentine's Day for example) instead of creating a new one. The new tickets for this year will replace the old ones (making the event upcoming again) and all of the customer reviews from previous years will still be shown.


The index page shows the next 3 upcoming events as well as cancelled events and has a search bar and category selector. These two parameters can be combined. Searching "Brisbane Festival" and "all categories", then filtering those results to "Brisbane Festival" + "Fireworks" is a good way to see that this works.
https://iab207thewheel.herokuapp.com/events/?search=Brisbane+Festival&category=all
https://iab207thewheel.herokuapp.com/events/?search=Brisbane+Festival&category=Fireworks
