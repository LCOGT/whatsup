FROM python:3.11-alpine

# Work within directory /app
WORKDIR /app

# install Python dependencies
COPY requirements.txt .
RUN apk --no-cache add postgresql-client \
        && apk --no-cache add --virtual .build-deps g++ gcc musl-dev postgresql-dev \
        && pip --no-cache-dir install -r requirements.txt \
        && pip --no-cache-dir install astropy \
        && apk --no-cache del .build-deps 

# install application
COPY . .

# default command
CMD [ "gunicorn", "--worker-class=gevent", "--workers=2", "--bind=0.0.0.0:8080", "--user=daemon", "--group=daemon", "--access-logfile=-", "--error-logfile=-", "whatsupapp.wsgi:application"]
