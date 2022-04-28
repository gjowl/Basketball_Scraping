My setup for this website came from this video: https://www.youtube.com/watch?v=dam0GPOAvVI&ab_channel=TechWithTim
Github for the beginner setup of this code: https://github.com/techwithtim/Flask-Web-App-Tutorial/tree/main/website

If you want to integrate your own javascript into this, put the setup files into the static folder (static images)
Once you put them into the status folder, add them using the below:
<script
  type="text/javascript"
  src="{{ url_for('static', filename='index.js') }}"
></script>
Add it to the bottom of the template body
url_for is a python function that finds the url and loads it to the website
"{{}}" This allows you to write a python expression in here that can be evaluated by jinja

HTTP: hyper text transfer protocol
Requests:
POST: updating or creating
GET: retrieving something
PUT, DELETE, etc. (write these somewhere)

Point of these is to clearly distinguish between what requests are being sent to your website so that the routes (on auth.py)
are going to the proper place.


How to determine 
We use http 

bootstrapping help: https://www.w3schools.com/Bootstrap/default.asp
