#!/bin/bash
export REPO_NAME=171453223611.dkr.ecr.eu-west-2.amazonaws.com
export AWS_DEFAULT_REGION=eu-west-2
export IMAGE_ID=$(docker images | grep testserver | grep latest | grep -v aws | awk '{print $3}'| uniq)
echo At this point you need the docker login you can get from 
echo aws ecr get-login-password, paste it then control-d at the prompt
read PASSWORD
export PASSWORD=$(aws ecr get-login-password)
docker login --username AWS --password $PASSWORD  ${REPO_NAME} 

docker tag $IMAGE_ID ${REPO_NAME}/testserver
docker push ${REPO_NAME}/testserver


