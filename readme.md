python -m venv env
env\Scripts\activate
pip install django
django-admin startproject core .
pip freeze > requirements.txt
pip install -r requirements.txt
pip install django mysqlclient

py manage.py migrate
py manage.py makemigrations
py manage.py createsuperuser
python manage.py startapp users
pip install djangorestframework
pip install django-cors-headers