FROM ubuntu:14.04
MAINTAINER Prashant Singh <prashant.vicky@gmail.com>
RUN apt update
#RUN apt upgrade
RUN apt install python2.7 python-pip
RUN apt install sysstat
ADD . /app
WORKDIR /app
