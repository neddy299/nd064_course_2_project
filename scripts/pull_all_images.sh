#!/bin/sh

# Delete pods and force image pull 

export SKIP_FRONTEND=true

echo -p "Preparing to delete pods to force image updates (ctrl-c to exit)" choice

kubectl delete pod $(kubectl get po | grep udaconnect-api | awk '{print $1}') & 
kubectl delete pod $(kubectl get po | grep udaconnect-locations | awk '{print $1}') &
kubectl delete pod $(kubectl get po | grep udaconnect-persons | awk '{print $1}') & 

if $SKIP_FRONTEND; then
    echo "Skipping frontend delete due to SKIP_FRONTEND = true"
else
    kubectl delete pod $(kubectl get po | grep udaconnect-app | awk '{print $1}') & 
fi
