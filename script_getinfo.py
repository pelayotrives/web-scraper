# 0.- We import the libraries.
import requests
import re
from bs4 import BeautifulSoup

# 1.- We declare the URL to scrap.
# 2.- We get the HTTP requests.
# 3.- We store it to manipulate them.
url = "https://www.eventbrite.es/d/spain--madrid/events/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 4.- We look for a characteristic class, in this case one of a card that contains the visible information of each event and saves the section it is in.
event_blocks = soup.find_all('section', class_='discover-vertical-event-card')

# 5.- We add the enumerate function to have an index.
for index, block in enumerate(event_blocks, start=1):
    # 6.- We request the name of the event. It is in a particular HTML tag with a unique class.
    event_name = block.find('h2', class_='Typography_body-lg__4bejd')
    if event_name:
        event_name = event_name.text.strip()

    # 7.- We request the date of the event. It is in a particular HTML tag with no-unique class, but we tag it as the only element without 2 particular classes.
    event_date = block.select_one('p:not(.eds-text-color--ui-600):not(.eds-text-color--ui-800)')
    if event_date:
        event_date = event_date.text.strip()

    # 8.- We request the location of the event. It is also in a particular HTML tag with a unique class.
    event_location = block.find('p', class_='eds-text-color--ui-600')
    if event_location:
        event_location = event_location.text.strip()

    print(f"Evento {index}")
    print(f"Nombre: {event_name}")
    print(f"Fecha: {event_date}")
    print(f"Lugar: {event_location}")
    print("--------")