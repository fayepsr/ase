::bat file for Windows Environment

docker stop annotation_container

docker rm annotation_container

docker image rm annotation_image:1.0

::Builds the docker image from python and php. 
::It will also copy the php and python files
docker build -f .\Dockerfile.dockerfile -t annotation_image:1.0 .


docker-compose -f .\annotation.yaml up