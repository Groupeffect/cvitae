FROM docker.io/groupeffect/django:primary
ENV PYTHONUNBUFFERD=0
RUN apt-get update && apt-get dist-upgrade -y
WORKDIR /app
COPY ./app /app
RUN pip install -r requirements.txt
EXPOSE 8000