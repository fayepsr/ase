
::docker stop annotation_container

::#docker rm annotation_container

doker-compose down

docker image rm charl/src_php:latest
docker image rm charl/charl/src_learner:latest
docker image rm charl/src_react:latest

cd ./src_react
docker build -f ./dockerfile -t charl/src_react:latest .

cd ../src_php
docker build -f ./dockerfile -t charl/src_php:latest .

cd ../src_learner
docker build -f ./dockerfile -t charl/src_learner:latest .

cd ../

docker-compose up
