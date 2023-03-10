# Social Networking Site

### Work done:

- [x] Login implemented
- [x] Need to implement register page

### Left to do:

- [ ] Use postgresql instead of sqlite
- [ ] Change structure of login urls
- [ ] Make register show errors
- [ ] Think if its better to use different class for users(Not same as Django Admin uses)
 
### Notes:

- To register an account use the admin, or command 'createsuperuser'
- To create user for admin, use 'createsuperuser'
- Remember to make migrations to DB
- Other less important fixes noted in files.

## What does the code do?
Django uses models to handle all types of data, for now I'm using model 'User' which is overwriting the User model that Django uses.<br>
Every model is connected to a Database, so there's no need to use SQLAlchemy for example, Django handles the migrations to the database with commands:
```
python manage.py makemigrations
python manage.py migrate
```
These commands must be run everytime there is a change in the models.
Also if an app is added to the project, must run
```
python manage.py makemigrations name_of_new_app
```

To create an __admin user__ which also works as a webpage user, just use command:
```
python manage.py createsuperuser
```

To run the project:
```
python manage.py runserver 
```
or
```
python manage.py runserver 'port'
```

Once an app is created, it has its own folder, for now we have apps called 'login' and 'mainpage', each app has urls(managed in urls.py), these urls connect to __views__ which are other component of Django, a __view__ is the way Django handles and renders each html file.

Basically for every part of the project, there's only need to modify the respective app.

And modify some things in settings.py if necessary.