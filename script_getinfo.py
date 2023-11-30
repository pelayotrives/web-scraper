from colorama import Fore, Style
from bs4 import BeautifulSoup
import requests
import sys
import time
import random
import os
import json

# As in the URL only the name of the city changes, we are going to make it dynamic by asking the user to enter the one he/she wants and from there the request is made.
city = input("Enter the name of the city: ")

# We declare the URL to scrap.
# We get the HTTP requests with the dynamic value.
# We store it to manipulate them.
url = f"https://www.eventbrite.es/d/spain--{city.lower()}/events/"

try:
    response = requests.get(url)
    # Verifies if the answer is successful.
    response.raise_for_status()
except requests.exceptions.HTTPError as errh:
    # If the answer is not successful, prints the error and closes the program.
    print("HTTP error:", errh)
    sys.exit(1)
except requests.exceptions.ConnectionError as errc:
    # If the answer is not successful, prints the error and closes the program.
    print("Connection error:", errc)
    sys.exit(1)
except requests.exceptions.Timeout as errt:
    # If the answer is not successful, prints the error and closes the program.
    print("Timeout error:", errt)
    sys.exit(1)
except requests.exceptions.RequestException as err:
    # If the answer is not successful, prints the error and closes the program.
    print("Error:", err)
    sys.exit(1)

soup = BeautifulSoup(response.text, 'html.parser')

# We look for a characteristic class, in this case one of a card that contains the visible information of each event and saves the section it is in.
event_blocks = soup.find_all('section', class_='discover-vertical-event-card')

# This is to store unique information of events and avoid duplicates.
processed_events = set()

# We add the enumerate function to have an index.
for index, block in enumerate(event_blocks, start=1):
    # Add a random pause between 2 and 5 seconds
    time.sleep(random.uniform(2, 5))

    # We request the name of the event. It is in a particular HTML tag with a unique class.
    event_name = block.find('h2', class_='Typography_body-lg__4bejd')
    event_name = event_name.text.strip() if event_name else ''
    # We request the date of the event. It is in a particular HTML tag with no-unique class, but we tag it as the only element without 2 particular classes.
    event_date = block.select_one('p:not(.eds-text-color--ui-600):not(.eds-text-color--ui-800)')
    event_date = event_date.text.strip() if event_date else ''
    # We request the location of the event. It is also in a particular HTML tag with a unique class.
    event_location = block.find('p', class_='eds-text-color--ui-600')
    event_location = event_location.text.strip() if event_location else ''
    # We request the link of the event. 
    event_link = block.find('a', class_='event-card-link')
    event_link = event_link['href'] if event_link else ''

    # This creates a tuple with the information of the event.
    event_info = (event_name, event_date, event_location, event_link)

    # Verify if the event has already been processed.
    if event_info not in processed_events:
        processed_events.add(event_info)
        # Fore.color + ... adds color to that line. Style.RESET_ALL + ... deletes that color to not show in the next ones.
        print(Fore.GREEN + f"Event {index}")
        print(Style.RESET_ALL + f"Name: {event_name}")
        print(f"Date: {event_date}")
        print(f"Place: {event_location}")
        print(f"Link: {event_link}")
        print("--------")

# Create the 'info' folder if it does not exist
if not os.path.exists('info'):
    os.makedirs('info')

# Prepare the data for the JSON file
data_to_export = {}
for i, event in enumerate(processed_events):
    data_to_export[i] = {
        'name': event[0],
        'date': event[1],
        'location': event[2],
        'link': event[3]
    }

# Name of the JSON file
json_filename = f"events_{city.lower()}.json"

# Save the data in a JSON file
with open(os.path.join('info', json_filename), 'w', encoding='utf-8') as f:
    json.dump(data_to_export, f, ensure_ascii=False, indent=4)

print(Fore.GREEN + f"Data saved to {json_filename} in 'info' directory.")
