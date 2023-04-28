
# # Check if Daniel Odier has announced any new Seminars
# If there are new seminars, make sure that I know about it by sending me an email using reminder@posturepower.de

import csv
import re
import requests
# %pip install beautifulsoup4 
from bs4 import BeautifulSoup
import smtplib
from configparser import ConfigParser, ExtendedInterpolation


config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('email.ini')



# Define the URL and other parameters
url = "https://danielodier.com/en/seminars-list"

# Set the sender and receiver email addresses
sender_email = "reminder@posturepower.de"
receiver_emails = ["eero.olli@gmail.com", "info@posturepower.de"]

password = config['EMAIL']['password']
smtp_server=config['EMAIL']['smtp_server']
smtp_port=465
sender_email=config['EMAIL']['username']


try:
    # resp = request.urlopen(url)
    resp = requests.get(url)
except Exception as ex:
    print(ex)
else:
    body = BeautifulSoup(resp.content, "html.parser")
finally:
    if resp is not None:
        resp.close()   
        print("Content of webpage is downloaded.")




events = body.find_all("a", class_="btn btn-prenota")

with open('odier_seminars.csv', mode='r') as file:
    reader = csv.DictReader(file)
    saved_seminars = [row for row in reader]

# Extract the highest number from the saved seminars
saved_seminars_numbers = [int(seminar['number']) for seminar in saved_seminars]
max_saved_number = max(saved_seminars_numbers)


# Create a list of dictionaries to store the online events
events_online = []

for event in events:
    event_str = str(event)
    match = re.search(r'/Seminar/(\d+)/(.*)(" type.*)', event_str)
    if match:
        number = int(match.group(1))
        name = str(match.group(2))
        events_online.append({'number': number, 'name': name})

# Extract the highest number from the online events
online_seminars_numbers = [event['number'] for event in events_online]
max_online_number = max(online_seminars_numbers)

# Compare the highest numbers and print the result
if max_saved_number >= max_online_number:
    print("No new seminars")

# New seminar: write csv and send email
else:
    new_seminar = next(event for event in events_online if event['number'] == max_online_number)
    print(f"There is a new seminar: {new_seminar['name']}")
# Send an email to notify about the new seminar
    message = f"""\
Subject: New Seminar Available

There is a new seminar available: {new_seminar['name']}
You should check: {url}


This email is sent with the script check_odiers_website
Best,
Eero
"""

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, password)
        for receiver_email in receiver_emails:
            server.sendmail(sender_email, receiver_email, message)

    # Replace the saved csv file with the updated online events
    with open('odier_seminars.csv', mode='w') as file:
        fieldnames = ['number', 'name']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for event in events_online:
            writer.writerow(event)

