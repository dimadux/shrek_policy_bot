FROM library/python:3.6

RUN apt-get -y update
RUN apt-get install -y python-pip python-dev build-essential
RUN pip install pymongo
RUN pip install telebot
RUN pip install Flask Jinja2 requests

RUN pip install pandas numpy scipy

WORKDIR /app