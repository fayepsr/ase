## Installation

```bash
docker build -f .\Dockerfile.dockerfile -t annotation_image:1.0 .
docker-compose -f .\annotation.yaml up
```
In case of Windows OS simply run 
```bash
.\docker_compose.bat
```

## Python example
Visit http://localhost:8089/python_model.php on your browser and an example from the python model will be ran.


## JAVA example 
Visit http://localhost:8089/java_model.php on your browser and an example from the python model will be ran.


### Docker
At the moment we are using multi-stage build.
To install JAVA: We create an image from openjdk:17 and then we copy the necessary files to run JAVA in the second image. We have also set the JAVA_HOME variable
Needed files: We have copied the necessary files using the COPY command
Install python and requirements: We have installed python and the requirements using the run command. 
The pip install -r /home/src_python/requirements.txt takes some time as it downloads some heavy requirements. 

```
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
```

### AWS lightsail
To push the image to Amazon lightsail
```bash
aws lightsail push-container-image --service-name ase-service-1 --label annotation-container --image annotation_image:1.0
```
Our public domain https://ase-service-1.iugkfeabdb168.eu-central-1.cs.amazonlightsail.com/python_model.php & https://ase-service-1.iugkfeabdb168.eu-central-1.cs.amazonlightsail.com/java_model.php 