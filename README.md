# check_odier_seminar

The purpose of these scripts is just to check a website, see if there are any new seminars announced, and if so send me an email about it.

Edit email.ini to match your own smtp setup using the configparser formating rules. https://docs.python.org/3.8/library/configparser.html  
The contents should be something like this:
<pre>
[EMAIL]
smtp_server="my.smpt.server.com"
smtp_port=465
username="usually@server.com"
sender_email=['username']
password="xxxxxxxxxx"
</pre>

Edit check_odiers_website.py 
* url and all other parameters 
* change the text of the email match your needs 

I have a cron job running on WLS that runs the check_changes_in_webpage.sh once a day.
* in WLS type crontab -e
* add your the path to your script that is run at fixed intervals
