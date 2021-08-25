#!/bin/bash

export AWS_DEFAULT_REGION=eu-west-2
export pod=""
export SERVER=""
if [ $1 == "enclave" ]
then 
  echo Deleting echoserver
  kubectl -n foo delete svc echoserver
  kubectl -n foo delete deploy echoserver
  echo deploying echoserver into enclave
  kubectl -n foo apply -f echoserver-nodebug-deployment.yaml
  kubectl -n foo apply -f Nodeport.yaml
  sleep 5
  while [ -z $pod ]
  do 
    export pod=$(kubectl -n foo get pods | grep Running | grep -m1 echoserver | awk '{print $1}')
    sleep 5  
  done
  echo $pod
  if [ -n "$(kubectl -n foo exec -it $pod -- ls | grep -v echoserver.py)" ]
  then 
    echo 'SUCCESS. Parent pod running. YOU WILL HAVE TO WAIT FOR THE ENCLAVE TO BUILD'
  else
    echo "ERROR Found python file in root. Is it in an enclave?"
    exit
  fi
  while [ -z "$SERVER" ]
  do 
    export SERVER="$(kubectl -n foo logs $(kubectl -n foo get pods | grep Running | grep -m1 echoserver | awk '{print $1}') | grep 'Server loop')"
    sleep 5
  done
  if [ "${SERVER}" == "INFO:__main__:Server loop running in thread: Thread-1" ]
  then 
    echo 'Enclave has started listener process'
    echo 'Getting service'
    ADDRESS=$(kubectl -n foo get endpoints -o json  | jq '.items[0].subsets[0].addresses[0].ip')
    PORT=$(kubectl -n foo get endpoints -o json  | jq '.items[0].subsets[0].ports[0].port')
    echo 'Enclave enabled pod is up on ' ${ADDRESS}:${PORT} ', you may continue'
  else
    echo "It broke, enclave hasn't returned correct messages. It may be ok though, check the logs with kubectl -n foo " ${pod} 
  fi

fi




if [ $1 == "noenclave" ]
then
  echo Deleting echoserver
  kubectl -n foo delete svc echoserver
  kubectl -n foo delete deploy echoserver
  echo deploying echoserver without enclave
  kubectl -n foo apply -f echoserver-noenclave-deployment.yaml
  kubectl -n foo apply -f Nodeport.yaml
  sleep 5
  while [ -z $pod ]
  do 
    export pod=$(kubectl -n foo get pods | grep Running | grep -m1 echoserver | awk '{print $1}')
    sleep 5  
  done
  echo $pod
  if [ -n "$(kubectl -n foo exec -it $pod -- ls | grep -m1 echoserver.py)" ]
  then 
    echo 'SUCCESS. Pod NOT running in enclave'
    echo 'Getting service'
    ADDRESS=$(kubectl -n foo get endpoints -o json  | jq '.items[0].subsets[0].addresses[0].ip')
    PORT=$(kubectl -n foo get endpoints -o json  | jq '.items[0].subsets[0].ports[0].port')
    echo 'Enclave enabled pod is up on ' ${ADDRESS}:${PORT} ', you may continue'
  else
    echo "ERROR: Couldn't find the python file. Check what's in the pod"  
  fi
fi