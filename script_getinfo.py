# HTTP requests to web
import requests
# Adds color to our script
from colorama import Fore
# To use regular expression
import re

# 1.- We declare the URL to scrap.
# 2.- We get the HTTP requests.
# 3.- We store it to manipulate them.
url = "https://www.eventbrite.es/d/spain--madrid/events/"
getEvents = requests.get(url)
events = getEvents.text

# 4.- We set a RegEx to get the main part of the URL.
# 5.- We find the repeated events.
# 6.- We set a list with no duplicates.
pattern = r"/e/([\w-]+)-\d+\b"
repeatedEvents = re.findall(pattern, str(events))
noDuplicates = list(set(repeatedEvents))

# 6.- We loop over our non-duplicated-elements list and print individually each event. 
for event in noDuplicates:
    eventNames = re.sub(r'entradas-', '', event).replace('-', ' ').title()
    print(eventNames)
