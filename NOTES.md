# Building images

Run the `build_images.sh` script to build all the images.

> NOTE: Before executing script: in the `build_images.sh` script, modify the docker REPO path `export REPO=nedd29` to your match REPO name 

```shell
./scripts/build_images.sh 
```

# Development

Before launching the modules in your development environment, you will need to copy the protobuf files into your modules. The `copy_protobuf.sh` helper script will do this for you

```shell
./scripts/copy_protobuf.sh 
```

> All modifications to protobuf files should be performed in the root `./protobufs` folder. After updating, re-run the script to update the modules. The docker build scripts will automatically import the latest protobuf files from the protobufs folder.

## Updating gRPC
```
cd protobufs
python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ udaconnect.proto
```

# Usefull commands

## API
```
kubectl exec -it $(kubectl get po | grep udaconnect-api | awk '{print $1}') -- sh
kubectl logs -f $(kubectl get po | grep udaconnect-api | awk '{print $1}')
kubectl delete pod $(kubectl get po | grep udaconnect-api | awk '{print $1}')
```

## Frontend
```
kubectl exec -it $(kubectl get po | grep udaconnect-app | awk '{print $1}') -- sh
kubectl logs -f $(kubectl get po | grep udaconnect-app | awk '{print $1}')
kubectl delete pod $(kubectl get po | grep udaconnect-app | awk '{print $1}')
```

## Locations
```
kubectl exec -it $(kubectl get po | grep udaconnect-locations | awk '{print $1}') -- sh
kubectl logs -f $(kubectl get po | grep udaconnect-locations | awk '{print $1}')
kubectl delete pod $(kubectl get po | grep udaconnect-locations | awk '{print $1}')
```

## Persons
```
kubectl exec -it $(kubectl get po | grep udaconnect-persons | awk '{print $1}') -- sh
kubectl logs -f $(kubectl get po | grep udaconnect-persons | awk '{print $1}')
kubectl delete pod $(kubectl get po | grep udaconnect-persons | awk '{print $1}')
```

# Misc Notes

## Windows kubectl and portfowarding
https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/

```
set KUBECONFIG=%userprofile%\.kube\config-udacity.yaml
kubectl port-forward service/udaconnect-app 30000:3000
kubectl port-forward service/udaconnect-api 30001:5000
kubectl port-forward service/udaconnect-persons 30002:5005
kubectl port-forward service/udaconnect-locations 30003:5005
```

## Fix database sequence gaps, helps prevents pkey conflicts
```
SELECT setval('location_id_seq', 100, FALSE);
SELECT setval('person_id_seq', 100, FALSE);
```