# 0.- We import the libraries.
import requests
from colorama import Fore, Style
from bs4 import BeautifulSoup

# 1.- We declare the URL to scrap.
# 2.- We get the HTTP requests.
# 3.- We store it to manipulate them.
url = "https://www.eventbrite.es/d/spain--madrid/events/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 4.- We look for a characteristic class, in this case one of a card that contains the visible information of each event and saves the section it is in.
event_blocks = soup.find_all('section', class_='discover-vertical-event-card')

# 5.- This is to store unique information of events and avoid duplicates.
processed_events = set()

# 6.- We add the enumerate function to have an index.
for index, block in enumerate(event_blocks, start=1):
    
    # 7.- We request the name of the event. It is in a particular HTML tag with a unique class.
    event_name = block.find('h2', class_='Typography_body-lg__4bejd')
    if event_name:
        event_name = event_name.text.strip() if event_name else ''
    # 8.- We request the date of the event. It is in a particular HTML tag with no-unique class, but we tag it as the only element without 2 particular classes.
    event_date = block.select_one('p:not(.eds-text-color--ui-600):not(.eds-text-color--ui-800)')
    if event_date:
        event_date = event_date.text.strip() if event_date else ''
    # 9.- We request the location of the event. It is also in a particular HTML tag with a unique class.
    event_location = block.find('p', class_='eds-text-color--ui-600')
    if event_location:
        event_location = event_location.text.strip() if event_location else ''
    # 10.- We request the link of the event. 
    event_link = block.find('a', class_='event-card-link')
    if event_link:
        event_link = event_link['href'] if event_link else ''

    # 11.- This creates a tuple with the information of the event.
    event_info = (event_name, event_date, event_location, event_link)

    # 12.- Verify if the event has already been processed.
    if event_info not in processed_events:
        processed_events.add(event_info)
        # 13.- Fore.color + ... adds color to that line. Style.RESET_ALL + ... deletes that color to not show in the next ones.
        print(Fore.GREEN + f"Event {index}")
        print(Style.RESET_ALL + f"Name: {event_name}")
        print(f"Date: {event_date}")
        print(f"Place: {event_location}")
        print(f"Link: {event_link}")
        print("--------")