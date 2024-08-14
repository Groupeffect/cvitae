#!/bin/sh
mig(){
    python manage.py makemigrations
    python manage.py migrate
}
dump(){
    # save api data to seperate json files
    python manage.py dumpdata api.photo --format=json -o apiphotodump.json
    python manage.py dumpdata api --exclude=api.photo --format=json -o apidump.json
}
load(){
    # load the saved dumps to database
    python manage.py loaddata --app=api --format=json apiphotodump.json
    python manage.py loaddata --app=api --format=json apidump.json
}
run(){
    # run server
    python manage.py runserver 0.0.0.0:8000
}
flush(){
    # delete database tables
    python manage.py flush --noinput
}
createsuperuser(){
    python manage.py createsuperuser
}
load_demo(){
    # demo setup 
    mig
    createsuperuser
    python manage.py loaddata --app=api --format=json demodump.json
    run
}
dump_demo(){
    # save demo data to json file
    python manage.py dumpdata api.templateconfig api.person api.address --format=json -o demodump.json
}
join_pdfs(){
	# gs -q -sPAPERSIZE=letter -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=output.pdf file1.pdf file2.pdf
	gs -q -sPAPERSIZE=letter -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=output.pdf $1 $2
}
cmd_simple_install(){
    # simple cli installation for demo setup with virtual environment based on venv
    python -m venv cvenv
    source cvenv/bin/activate
    pip install -r requirements.txt
    load_demo && run
}
