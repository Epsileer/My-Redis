create a virtual environment to isolate our package dependencies locally</br>
<b>python -m venv env</b>

To activate the environment in windows</br>
<b>env\Scripts\activate</b>

Install dependencies</br>
<b>pip install Django</b>
<b>pip install sortedcontainers</b>

After sussessful installation of Django you get a new command django-admin</br>

<b>django-admin startproject redis</b>

to create an app</br>
<b>django-admin startapp myapp</b>

The four files we care about are</br>
redis/setting.py</br>
redis/urls.py</br>
redis/myapp/views.py</br>
redis/myapp/models.py</br> 

In setting.py add an app you just created in INSTALLED_APPS</br>
INSTALLED_APPS = [</br>
    .....</br>
    'myapp'</br>
]</br>

Copy and paste the code from redis/myapp/models.py.</br>
we want to convert these models into sql tables and to do so while changing models run migrations.</br>

<b>python manage.py makemigrations</b></br>
<b>python manage.py makemigrations myapp</b></br>
<b>python manage.py migrate</b></br>


Create two new files redis/myapp/singleton.py and redis/myapp/zsingleton.py.</br>

Now copy and paste each files code...</br>
<b>redis/urls.py</b></br>
<b>redis/myapp/singleton.py</b></br>
<b>redis/myapp/zsingleton.py</b></br>
<b>redis/myapp/views.py</b></br>

To run the server</br>
<b>python manage.py runserver</b></br>


Now to check the running project install 'Postman' and hit different urls like..</br>

<b>https://localhost:8000/get/key</b></br>
<b>https://localhost:8000/set</b></br>
<b>https://localhost:8000/key/ttl</b></br>
<b>https://localhost:8000/zadd</b></br>
<b>https://localhost:8000/zrank/key/value</b></br>
<b>https://localhost:8000/zrange/l/r</b></br>
