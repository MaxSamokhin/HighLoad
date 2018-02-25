FROM ubuntu:16.04

MAINTAINER Samokhin Max
USER root

RUN apt-get -y update
RUN apt-get install -y python3

ADD ./ /var/www/html/
CMD python3 /var/www/html/public/main.py -r /var/www/html

EXPOSE 80
