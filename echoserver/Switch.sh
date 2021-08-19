#!/bin/bash

export AWS_DEFAULT_REGION=eu-west-2
export pod=""
if [ $1 == "enclave" ]
then 
  echo Deleting testserver
  kubectl -n foo delete svc testserver
  kubectl -n foo delete deploy testserver
  echo deploying testserver into enclave
  kubectl -n foo apply -f testserver-deployment.yaml
  kubectl -n foo apply -f load-balancer.yaml
  sleep 5
  while [ -z $pod ]
  do 
    export pod=$(kubectl -n foo get pods | grep Running | grep -m1 testserver | awk '{print $1}')
    sleep 5  
  done
  echo $pod
  if [ -n "$(kubectl -n foo exec -it $pod -- ls | grep -v testserver.py)" ]
  then 
    echo 'SUCCESS. Pod running in enclave'
  else
    echo "Is it in an enclave?"
  fi
fi

if [ $1 == "noenclave" ]
then
  echo Deleting testserver
  kubectl -n foo delete svc testserver
  kubectl -n foo delete deploy testserver
  echo deploying testserver without enclave
  kubectl -n foo apply -f testserver-noenclave-deployment.yaml
  kubectl -n foo apply -f load-balancer.yaml
  sleep 5
  while [ -z $pod ]
  do 
    export pod=$(kubectl -n foo get pods | grep Running | grep -m1 testserver | awk '{print $1}')
    sleep 5  
  done
  echo $pod
  if [ -n "$(kubectl -n foo exec -it $pod -- ls | grep -m1 testserver.py)" ]
  then 
    echo 'SUCCESS. Pod NOT running in enclave'
  else
    echo "Couldn't find the python file"
  fi
fi