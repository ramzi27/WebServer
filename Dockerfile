FROM python:3.7.4-alpine3.10
RUN  mkdir /app
WORKDIR /app
COPY . .
CMD python webserver.py
