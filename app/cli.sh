#!/bin/sh
mig(){
    python manage.py makemigrations
    python manage.py migrate
}
dump(){
    python manage.py dumpdata api.photo --format=json -o apiphotodump.json
    python manage.py dumpdata api --exclude=api.photo --format=json -o apidump.json
}
load(){
    python manage.py loaddata --app=api --format=json apiphotodump.json
    python manage.py loaddata --app=api --format=json apidump.json
}
run(){
    python manage.py runserver 0.0.0.0:8000
}
flush(){
    python manage.py flush --noinput
}
createsuperuser(){
    python manage.py createsuperuser
}
load_demo(){
    mig
    createsuperuser
    python manage.py loaddata --app=api --format=json demodump.json
    run
}
dump_demo(){
    python manage.py dumpdata api.templateconfig api.person api.address --format=json -o demodump.json
}
join_pdfs(){
	# gs -q -sPAPERSIZE=letter -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=output.pdf file1.pdf file2.pdf
	gs -q -sPAPERSIZE=letter -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=output.pdf $1 $2
}
