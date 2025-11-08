#!/usr/bin/bash

# This is a helperscript designed to remove any container or volume by the ocr service
# to build new ones in case code/version has changed

docker-compose down
docker stop "$(docker ps -q)"
docker rm "$(docker ps -aq --filter "name=ocr")"
docker volume rm "$(docker volume ls -q --filter "name=ocr")"
docker rmi -f "$(docker images -q --filter "reference=*ocr*")"
