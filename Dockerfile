FROM docker.io/groupeffect/django:primary
ENV PYTHONUNBUFFERD=1
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update && apt-get dist-upgrade -y
WORKDIR /app
COPY ./app /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000