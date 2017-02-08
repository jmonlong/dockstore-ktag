# Set the base image to Ubuntu
FROM ubuntu:14.04

# File Author / Maintainer
MAINTAINER Jean Monlong <jean.monlong@gmail.com>

# Setup packages
USER root
RUN apt-get -m update && apt-get install -y python curl 

# Install latest version of pip
RUN curl  https://bootstrap.pypa.io/get-pip.py | sudo python

# Install Python modules
RUN pip install pysam sklearn

# Copy the python script to /usr/local/bin
COPY ktag.py /usr/local/bin/
RUN chmod a+x /usr/local/bin/ktag.py

# Switch back to ubuntu user
RUN groupadd -r -g 1000 ubuntu && useradd -r -g ubuntu -u 1000 -m ubuntu
USER ubuntu

CMD ["/usr/local/bin/ktag.py"]
