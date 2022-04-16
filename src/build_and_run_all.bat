
docker-compose down

docker image rm src_php:latest
docker image rm src_learner:latest
docker image rm src_react:latest

cd ./src_react
docker build -f ./dockerfile -t src_react:latest . 

cd ../src_php
docker build -f ./dockerfile -t src_php:latest .

cd ../src_learner
docker build -f ./dockerfile -t src_learner:latest .

cd ../

docker-compose up
