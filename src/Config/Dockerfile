FROM python:3.7-buster

ENV TZ=Asia/Tokyo

WORKDIR /usr/src/app

RUN apt-get update
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000