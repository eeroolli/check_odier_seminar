
# # Check if Daniel Odier has announced any new Seminars
# If there are new seminars, make sure that I know about it by sending me an email using reminder@posturepower.de
# this script runs in the conda env ds.

import csv
import re
import requests
from bs4 import BeautifulSoup
import smtplib
from configparser import ConfigParser, ExtendedInterpolation
from datetime import datetime
from os import path


config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('/keybase/private/eeroolli/secrets_for_python.ini')   #encrypted and safeguarded by keybase
#print(f"These are the sections: {config.sections()}")

print(f"Running the script '{path.basename(__file__)}'")

#### Define ==========================

# Define the URL and other parameters
URL = "https://danielodier.com/en/seminars-list"

SEMINARS_CSV = "odier_seminars.csv"  # This is where the previous info is saved.

SENDER_EMAIL = "reminder@posturepower.de"
receiver_emails = ["eero.olli@gmail.com", "info@posturepower.de"]

PASSWORD = config['EMAILREMINDER']['password']
SMTP_SERVER=config['EMAILREMINDER']['smtp_server']
SMTP_PORT=465
SENDER_EMAIL=config['EMAILREMINDER']['username']


#### ==============================
try:
    # resp = request.urlopen(url)
    resp = requests.get(URL)
except Exception as ex:
    print(ex)
else:
    body = BeautifulSoup(resp.content, "html.parser")
finally:
    if resp is not None:
        resp.close()   
        print("Content of webpage is downloaded.")


events = body.find_all("a", class_="btn btn-prenota")    # this class contain the seminars

#### Saved events ================================
# Extract the highest number from the saved seminars
with open(SEMINARS_CSV, mode='r') as file:
    reader = csv.DictReader(file)
    saved_seminars = [row for row in reader]
    file.close()

saved_seminars_numbers = [int(seminar['number']) for seminar in saved_seminars]
max_saved_number = max(saved_seminars_numbers)  # The assumption is that they number seminars in the order.
# I can imagine that there might be errors but I will not deal with them.


#### New events ================================

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


#### Compare the highest numbers and send email ============= 

if max_saved_number >= max_online_number:
    notification_text = f"There are no new seminars"
   

# New seminar: write csv and send email
else:
    new_seminar = next(event for event in events_online if event['number'] == max_online_number)
    notification_text = f"There is a new seminar: {new_seminar['name']}"
    
# Send an email to notify about the new seminar
    MESSAGE = f"""\
Subject: New Seminar Available

There is a new seminar available: {new_seminar['name']}
You should check: {URL}


This email is sent with the script check_odiers_website
Best,
Eero
"""

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        for receiver_email in receiver_emails:
            server.sendmail(SENDER_EMAIL, receiver_email, MESSAGE)

    # Replace the saved csv file with the updated online events if needed
    with open(SEMINARS_CSV, mode='w') as file:
        fieldnames = ['number', 'name']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for event in events_online:
            writer.writerow(event)
        file.close()

## Keep track of last successful run, as it is a cron script =========
dt = datetime.now().strftime("%A %d-%m-%Y %X ")
# print(dt)
print(f"{notification_text}")
with open('./last_run_was.txt', 'w') as f:
    f.write(f"{notification_text} at {dt}")
    f.close()