FROM python:3.6.8-alpine

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev

WORKDIR /opt/rmw

COPY Pipfile /opt/rmw
COPY Pipfile.lock /opt/rmw

RUN ["pip", "install", "pipenv"]
RUN ["pipenv", "install"]

RUN apk del build-deps

COPY . /opt/rmw
