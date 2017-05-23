# powerball2-django

on a Linux system:

cd into directory

run the virtualenv:

source/bin/activate

cd src

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py loaddata sites popular

python manage.py runserver

enter url:

http://127.0.0.1:8000/

to load entry data:

python manage.py loaddata entries most_popular
