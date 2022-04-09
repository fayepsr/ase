# 1. Create, build and run a single Docker container

Note: all commands are for windows

## 1.1 Create a dockerfile, e.g. for node.js:  https://nodejs.org/en/docs/guides/nodejs-docker-webapp/

Move to the folder where you want to create dockerfile
> cd C:\Users\charl\Documents

Create dockerfile
> touch dockerfile

Edit dockerfile with your favourite text editor
note that you can import a lot of templates with "FROM"; docker hub, container, image library etc.

## 1.2 Build and run the dockerfile

> docker build . -t python1

Explanation: command: docker build. The dot . specifies where the dockerfile is at.
-t specifies a tagname for the container we are building. 
We can set a lot more flags, see the doc. 
Doc: https://docs.docker.com/engine/reference/commandline/build/

>docker images

Explanation: shows the current images on this machine. Check that python1 exists and check its id.

>docker run -p 5000:9070 -d python1

Explanation: docker run; starts a container from image. -p redirects public port to private port
so if our e.g. flask API on the inside of the docker container is listening to the port 9070, then
this port gets redirected to the port 5000 on the outside -> if I want to call the flask api from
the outside of the container, I have to call port 5000, from the inside port 9070. -d choose image via tag name
and runs container in detached mode, leaving it running in the background. After running this command,
you should get back the container id (not to confuse with image id) which looks something like 
hjdsfkhsdojfdlhdsfjkh234jhdfhl9dfudhsj4zuieodsjfdnjbh8g948urj

>docker container list

Explanation: gives you a list of all the running containers. 

>docker logs CONTAINER_ID

Explanation: shows you the logs of a container. Important for debugging (e.g. is my API running)

## 1.3 Delete the docker container and image

> docker stop CONTAINER_ID
or
> docker kill CONTAINER_ID

Explanation: stops one or more running container via id. If gracefully shutting down the container
does not work, you can also kill it.

> docker rmi IMAGE_ID
or 
> docker rmi -f IMAGE_ID

Explanation: removes the image from your machine. Adding the f does so forcefully (e.g. if the image is used by
a container that is running).

> docker system prune
or
> docker system prune -all

Explanation: if after removing the images, the disk space is still used up by docker, try the two commands
above. If this does not help, restart your machine.

# 2. Docker-Compose Commands
can run one or more container, define ports and manage them -> basically a script for image and container building.

Move to the folder where you want to create dockerfile
> cd C:\Users\charl\Documents

## 2.1 Start docker-compose

> docker-compose up

Explanation: builds container from images (if this has not been done yet) and starts container. 
Also defines ports and volumes.

> docker-compose up -d --no-deps --build react1

Explanation: forces rebuild of specific service.

## 2.2 Stop docker-compose

> docker-compose down

Explanation: stops the containers. 

> wsl --shutdown

DANGEROUS! In case after stopping the containers, vmmem still uses up all your RAM, you can forcefully
shut it down. 

# 3. CURL commands for API testing

curl http://localhost:5000/?user=charl

curl http://127.0.0.1:5000/?user=charl

wsl --shutdown