FROM ubuntu:14.04
MAINTAINER Prashant Singh <prashant.vicky@gmail.com>
RUN apt update -y
RUN apt upgrade -y
RUN apt install -y python2.7 python-pip
RUN apt install -y sysstat
ADD app /app
WORKDIR /app
