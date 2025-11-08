#!/usr/bin/bash

# This is a helperscript to start the docker-compose

docker-compose down

rm ./.env
sleep 1
echo "OTEL_RESOURCE_ATTRIBUTES=service.instance.id=$(uuidgen)" >.env
sleep 1
docker-compose up
