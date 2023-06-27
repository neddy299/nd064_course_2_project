#!/bin/sh

# Build and optionally deploy images

export REPO=nedd29
export DEPLOY_IMAGES=true

echo "Building images"
docker build -t $REPO/nd064-udaconnect-api -f modules/api/Dockerfile .
docker build -t $REPO/nd064-udaconnect-app -f modules/frontend/Dockerfile .
docker build -t $REPO/nd064-udaconnect-locations -f modules/locations_service/Dockerfile .
docker build -t $REPO/nd064-udaconnect-persons -f modules/persons_service/Dockerfile .


if $DEPLOY_IMAGES; then
    echo "Deploying images"
    docker push $REPO/nd064-udaconnect-api
    docker push $REPO/nd064-udaconnect-app
    docker push $REPO/nd064-udaconnect-locations
    docker push $REPO/nd064-udaconnect-persons
fi