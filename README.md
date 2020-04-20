create a virtual environment to isolate our package dependencies locally
python -m venv env

To activate the environment in windows
env\Scripts\activate

Install dependencies
pip install Django
pip install sortedcontainers

After sussessful installation of Django you get a new command django-admin

django-admin startproject redis

to create an app
django-admin startapp myapp

The four files we care about are
redis/setting.py
redis/urls.py
redis/myapp/views.py
redis/myapp/models.py 

In setting.py add an app you just created in INSTALLED_APPS
INSTALLED_APPS = [
    .....
    'myapp'
]

Copy and paste the code from redis/myapp/models.py.
we want to convert these models into sql tables and to do so while changing models run migrations.

python manage.py makemigrations
python manage.py makemigrations myapp
pythn manage.py migrate


Create two new files redis/myapp/singleton.py and redis/myapp/zsingleton.py.

Now copy and paste each files code...
redis/urls.py
redis/myapp/singleton.py
redis/myapp/zsingleton.py
redis/myapp/views.py

To run the server
python manage.py runserver


Now to check the running project install 'Postman' and hit different urls like..

https://localhost:8000/get/key
https://localhost:8000/set
https://localhost:8000/key/ttl
https://localhost:8000/zadd
https://localhost:8000/zrank/key/value
https://localhost:8000/zrange/l/r
