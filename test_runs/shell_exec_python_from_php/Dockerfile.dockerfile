FROM php:7.4-apache AS php-apache

COPY src_php/ /var/www/html/
COPY src_python/ /home/python_example/
COPY src_java/ /home/java_example/


RUN chmod 755 /home/python_example/test.py && \
chmod 777 /home/java_example/ && \
apt update  && \
apt-get install -y python2.7 && \ 
apt update && \ 
apt install -y default-jre && \ 
apt install -y default-jdk