FROM openjdk:17 as builder1

#CMD tail -f /dev/null


FROM php:7.4-apache-bullseye AS php-apache
COPY --from=builder1 /usr/java/openjdk-17 /usr/java/openjdk-17
COPY ./var/www/html/ /var/www/html
COPY ./home/ /home

ENV JAVA_HOME /usr/java/openjdk-17
ENV PATH $JAVA_HOME/bin:$PATH

RUN cp /etc/apache2/mods-available/rewrite.load /etc/apache2/mods-enabled/ && \
cp /etc/apache2/mods-available/headers.load /etc/apache2/mods-enabled/  && \
chmod 755 /home/src_python/highlight.py && \
 apt update  && \
 apt-get install -y python3.9 && \ 
 apt update && \ 
 apt install -y pip && \ 
 pip install -r /home/src_python/requirements.txt
