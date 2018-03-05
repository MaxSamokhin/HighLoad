FROM ubuntu:16.04

MAINTAINER Samokhin Max
USER root

RUN apt-get -y update
RUN     apt-get install -y python3

ADD ./ /var/www/html/
ADD ./httpd.conf /

#RUN python3 -m pip install -r /var/www/html/req.txt
CMD python3 /var/www/html/public/main.py

EXPOSE 80
