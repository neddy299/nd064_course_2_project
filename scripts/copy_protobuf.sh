#!/bin/sh

# Copy protobuf files into modules

cp protobufs/udaconnect* ./modules/api
cp protobufs/udaconnect* ./modules/locations_service
cp protobufs/udaconnect* ./modules/persons_service
cp protobufs/udaconnect* ./tests