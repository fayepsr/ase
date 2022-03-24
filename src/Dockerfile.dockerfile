FROM php:7.4-apache AS php-apache

COPY src_php/ /var/www/html/
COPY src_python/ /home/src_python/
COPY src_java/ /home/src_java/
COPY UZH-ASE-AnnotationWS-BaseLearner/*.py /home/src_python/
COPY UZH-ASE-AnnotationWS-FormalModel/Library/SHOracle.jar /home/src_java/


RUN chmod 755 /home/src_python/shmodel.py && \
chmod 777 /home/src_java/ && \
apt update  && \
apt-get install -y python3.9 && \ 
apt update && \ 
apt install -y openjdk-11-jre && \ 
apt install -y openjdk-11-jdk && \
apt update && \ 
apt install -y pip && \ 
pip install -r /home/src_python/requirements.txt

#alternatively: https://felixgondwe.medium.com/set-java-home-on-ubuntu-docker-container-e302a7aa45ad
# or ENV JAVA_HOME /path/to/java