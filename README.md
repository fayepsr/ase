## Functionality
Our implementation at this point accepts a POST request at {{URL}}/api/v1/highlight and prints the prediction as an array of HcodeValues

## Installation

Make sure you navigate inside src folder

```bash
docker build -f .\Dockerfile.dockerfile -t annotation_image:1.0 .
docker-compose -f .\annotation.yaml up
```
In case of Windows OS simply run 
```bash
.\docker_compose.bat
```

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
```

### AWS lightsail
To push the image to Amazon lightsail
```bash
aws lightsail push-container-image --service-name ase-service-1 --label annotation-container --image annotation_image:1.0
```
Our public domain https://ase-service-1.iugkfeabdb168.eu-central-1.cs.amazonlightsail.com/

### Our directories

├───postman #This folder contains the postman collections. See how to import it here: https://learning.postman.com/docs/getting-started/importing-and-exporting-data/
├───src #The code to be ran inside the container
│   ├───home
│   │   └───src_python
│   └───var
│       └───www
│           └───html
│               ├───classes
│               └───public

