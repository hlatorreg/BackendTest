# Desarrollo Backend Test

### So far:

* Clone proyect
* Create virtualenv with python3.7
* Install requirements.txt
* Run migrations...
* python manage.py runserver -> starts app
* curl http://localhost:8000/api/v1/tasks/crawl -> send request to task, any other method returns error
* python manage.py process_tasks -> starts queue, should be run on a differemt shell