## Pre-requisites

Python version 3.8 or newer and mySql-dev header is required

get both using "sudo apt-get install python3-dev default-libmysqlclient-dev build-essential"


## Installation

# [Basics]
A Python3 virtual environment is strongly recommended and needed

# [Database]

Edit the DATABASE in "settings.py" of the mysite folder to specify your database settings
The project will create a Database with all the required Table for you the first time you run migrations

A MySQL-Database was used for this application, the Database is included under "Database Dump" and can be imported into existing Servers if needed.


# [Email]
Any Email that can be used via SMTP is usable with the crawler. A functioning Googlemail account is currently being used, but can be changed in the 'sendMail.py' file


# [Webapp]

1. Extract the folder into your desired directory

2. Open a terminal and navigate to the main folder

3. Run "pip install -r requirements.txt" to install all the dependencies

4. Edit the allowed hosts in "mysite/settings.py" of the mysite folder to allow host IP (e.g Gibybyte.com)

5. Edit the DATABASE in "mysite/settings.py" of the mysite folder to specify your database settings (default settings connect to a localhost Database with root)

6. Run "python3 manage.py makemigrations" and "python3 manage.py migrate" to automatically create a database/detect existing database

7. Run "python3 manage.py runserver YOUR_DOMIAN_OR_IP:PORT" to start the webserver


## Administration

1. Run python3 manage.py createsuperuser to create and register a Superuser before starting the Webapp

2. Access YOUR_DOMIAN_OR_IP:PORT/admin once you have started up the Webapp and login with the Superuser credentials

3. Now you are able to easily remove/add journals and manage Users



## Usage

# [via Terminal]

1. Crawl all the listed Websites by running "scrapy crawl combined" in the postscrapes folder via the terminal, the current issue will then be updated in the Database.

2. Run the "FIM_newsletter.py" script via the terminal to send out an Email to every Email listed in the Database.

# [via Webapp]

1. Log-in using an Superuser account (refer to #Administration)

2. Two more options will now appear on the dropdown menu

3. Choose your page and click the button to manually crawl/send out mails


## Automation

0. Visit https://crontab.guru/ to find a suitable schedule expression

1. Run "crontab -e" to open the Crontab configuration

2. Input a command/commands to execute after the expression



Example Crawler: 
59 23 * * * . /home/djangoserver/django_project/venv/bin/activate && cd /home/djangoserver/django_project/crawler/postscrape && scrapy crawl combined > /home/tim/crontab.log 2>&1

Example E-Mails:
59 23 * * * . /home/djangoserver/django_project/venv/bin/activate && cd /home/djangoserver/django_project && python FIM_newsletter.py > /home/tim/crontab.log 2>&1




