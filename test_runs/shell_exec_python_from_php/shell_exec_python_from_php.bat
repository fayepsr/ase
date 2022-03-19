::bat file for Windows Environment

docker stop example_container

docker rm example_container

docker image rm shell_exec_python_from_php:1.0

::Builds the docker image from python and php. 
::It will also copy the php and python files
docker build -f .\Dockerfile.dockerfile -t shell_exec_python_from_php:1.0 .


docker-compose -f .\shell_exec_python_from_php.yaml up

::docker exec -it ##container_id## bash