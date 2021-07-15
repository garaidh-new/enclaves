#!/bin/bash

export AWS_DEFAULT_REGION=eu-west-2

if [ $1 == "enclave" ]
then 
  echo Deleting testserver
  kubectl -n foo delete svc testserver
  kubectl -n foo delete deploy testserver
  echo deploying testserver into enclave
  kubectl -n foo apply -f testserver-deployment.yaml
  kubectl -n foo apply -f load-balancer.yaml
  export pod=$(kubectl -n foo get pods | grep -m1 testserver | awk '{print $1}')
  if [ -n "$(kubectl -n foo exec -it $pod -- ls | grep opt)" ]
  then 
    echo 'Pod running in enclave'
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
  export pod=$(kubectl -n foo get pods | grep -m1 testserver | awk '{print $1}')
  if [ -n "$(kubectl -n foo exec -it $pod -- ls | grep opt)" ]
  then 
    echo 'Pod running in enclave'
  fi
fi