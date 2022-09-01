FROM python:3.9.2-alpine

ENV PYTHONUNBUFFERED = 1

WORKDIR  /code

COPY requirements.txt .

RUN pip install -r requirements.txt 

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps

COPY . .

EXPOSE 8000

RUN ["python3","manage.py","runserver","0.0.0.0:8000"]

