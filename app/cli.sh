#!/bin/sh
mig(){
    python manage.py makemigrations
    python manage.py migrate
}

dump(){
    python manage.py dumpdata api --exclude=api.photo --format=json -o apidump.json
    python manage.py dumpdata api.photo --format=json -o apiphotodump.json
}

load(){
    python manage.py loaddata --app=api --format=json apidump.json apidump.json
    python manage.py loaddata --app=api --format=json apidump.json apiphotodump.json
}

run(){
    python manage.py runserver 0.0.0.0:8000
}