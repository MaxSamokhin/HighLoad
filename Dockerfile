FROM ubuntu:16.04

MAINTAINER Samokhin Max
USER root

RUN  apt-get -y update
RUN  apt-get install -y python3
RUN  apt-get -y install python3-pip
RUN  pip3 install urllib3


ADD . .

EXPOSE 80

CMD python3 public/main.py

