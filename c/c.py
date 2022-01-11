from icalendar import Calendar, Event
from datetime import datetime
import requests
import cgi
import cgitb

# save reports to log directory
cgitb.enable(display=1, logdir="/var/log/lighttpd/meeting.5066.team/")

open('/usr/local/www/meeting/calendar.ics', 'wb').write(requests.get("https://calendar.google.com/calendar/ical/c_25ivjnmvb250eunu4atfthd91s%40group.calendar.google.com/public/basic.ics").content)

print("Content-Type: text/html\n")

today = datetime.now()
t = False
with open("/usr/local/www/meeting/calendar.ics", "r") as f:
    cal = Calendar.from_ical(f.read())
    for component in filter(lambda x: x.name == "VEVENT", cal.walk()):
        dts = component["DTSTART"].dt
        dte = component["DTEND"].dt
        if hasattr(dts, "hour"):
            if today.day == dts.day and today.month == dts.month and today.year == dts.year:
                t = True

m = "<h2 class=\"yes\">Yes.</h2>" if t else "<h2 class=\"no\">No.</h2>"

print("""<!DOCTYPE html>
<html>
    <head>
        <title>Are we meeting?</title>
        <style>
                body {
                        text-align: center;
                }
                h2 {
                        font-size: 5em;
                }
                p {
                        font-size: 1.5em;
                }
                .yes {
                        color: green;
                }
                .no {
                        color: red;
                }
                .left {
                        text-align: left;
                        width: 50%;
                        margin: auto;
                }
                .time {
                        color: red;
                        font-weight: bold;
                }
                #are-we {
                        margin: auto;
                        width: 50%;
                        border: 3px solid black;
                }
            </style>
        </head>
    <body>
        <h1>are we meeting yet?</h1>
        <div id="are-we">""" + m + """</div>
        <p><a href="/s.html">full schedule</a></p>
    </body>
</html>""")

