#!/bin/bash
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity | grep Arn | awk -F: '{print $6}')
if [ -z $AWS_ACCOUNT_ID ]
then
    echo 'No AWS_ACCOUNT_ID or null, do we have creds?'
fi
export AWS_DEFAULT_REGION=eu-west-2
export REPO_NAME=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com
export IMAGE_ID=$(docker images | grep testserver | grep latest | grep -v aws | awk '{print $3}'| uniq)
echo At this point you need the docker login you can get from 
echo aws ecr get-login-password, paste it then control-d at the prompt, or don\'t if the instance has it
read PASSWORD
export PASSWORD=$(aws ecr get-login-password)
docker login --username AWS --password $PASSWORD  ${REPO_NAME} 

docker tag $IMAGE_ID ${REPO_NAME}/testserver
docker push ${REPO_NAME}/testserver


