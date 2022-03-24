FROM openjdk:17 as builder1

#CMD tail -f /dev/null


FROM php:7.4-apache-bullseye AS php-apache
COPY --from=builder1 /usr/java/openjdk-17 /usr/java/openjdk-17
COPY src_php/ /var/www/html/
COPY src_python/ /home/src_python/
COPY src_java/ /home/src_java/
COPY UZH-ASE-AnnotationWS-BaseLearner/*.py /home/src_python/
COPY UZH-ASE-AnnotationWS-FormalModel/Library/SHOracle.jar /home/src_java/
ENV JAVA_HOME /usr/java/openjdk-17
ENV PATH $JAVA_HOME/bin:$PATH

RUN chmod 755 /home/src_python/shmodel.py && \
chmod 777 /home/src_java/ && \
apt update  && \
apt-get install -y python3.9 && \
apt update && \ 
apt install -y pip && \ 
pip install -r /home/src_python/requirements.txt
