# Desarrollo Backend Test

### So far:

* Clone proyect and cd into it
* Create virtualenv with python3.7
* Activate your virtualenv with ```. virtualenv/bin/activate```
* Install requirements.txt, ```pip install -r requirements.txt```
* Run migrations...
* ```python manage.py runserver``` -> starts app
* Included a Postman collection, if you changed the port on the testing enviroment you shoud also change it on postman routes.
* After calling Start Scrapping from postman, you should run ```python manage.py process_task``` on a shell with virtualenv.