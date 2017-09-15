# django-eventlog
A simple example to show how simple log can be maintained in Django.


### Install the required packages using the following commands:

pip install eventlog


### Add eventlog to your INSTALLED_APPS setting:

INSTALLED_APPS = (

    #third-party apps
    'eventlog',
)


### Run the migrations and server:

python manage.py makemigrations

python manage.py migrate 

python manage.py runserver
