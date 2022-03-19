FROM php:7.4-apache AS php-apache

COPY src_php/ /var/www/html/
COPY src_python/ /home/python_example/


#RUN mkdir -p /scripts
#COPY bootstrap.sh /scripts
#WORKDIR /scripts
#RUN chmod +x bootstrap.sh
#RUN ./bootstrap.sh

RUN chmod 755 /home/python_example/test.py && \
apt update  && \
apt-get install -y python2.7 > test.txt && echo 1
