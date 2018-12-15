FROM ubuntu:16.04

# Install.
RUN \
  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  apt-get update -y && \
  apt-get install -y ruamel.yaml && \
  apt-get -y upgrade && \
  apt-get install -y build-essential && \
  apt-get install -y software-properties-common && \
  apt-get install -y byobu curl git htop man unzip vim wget && \
  #apt install -y python3.6 && \ 
  apt-get install -y python2.7 python-pip && \
  pip install -U pip setuptools wheel && \
  pip install -y ruamel.yaml && \
  apt-get install -y sysstat && \
  apt-get install -y net-tools && \
  apt-get install -y iputils-ping && \
  rm -rf /var/lib/apt/lists/*
CMD ["bash"]
