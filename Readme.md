# Jibambex API
A Django Rest Framework that generates Movies url's from a local storage and serves them to clients.
## Getting Started
Create a virtual environment to work on by running `virtualenv venv -p python3`. Activate It through `source venv/bin/activate` and then
Clone the repo by running `git clone git@github.com:esirK/JibambexApi.git` .

## Prerequisites
Change into the __JibambeApi__ folder and run `pip install -r requirements.txt` which will install all the required packages.
Now You almost there.

## Installing

To get you database ready, run `python manage.py makemigrations` then `python manage.py migrate`. You will need
a super user account during development which you can create through `python manage.py createsuperuser` . After you fill in the details that you are asked,
you can start the server by running `python manage.py runserver 0.0.0.0:8000` the *0.0.0.0:8000* will ensure that your server is listening on
all ports and can be accessed by any other user on the same network.
Access the running Api from http://127.0.0.1:8000/moviescategories/ to see available movie categories which are empty by default. To create some Movie Categories eg. __Action, Horror etc__, you can use the __Django Admin__  site to create some. Navigate to http://127.0.0.1:8000/admin/ and create some movies categories.
To access movies in a single category, navigate to http://127.0.0.1:8000/moviescategories/{id} where *id* is the id of the Movies category

## Authors
* **Isaiah Ngaruiya** - *Initial work*
