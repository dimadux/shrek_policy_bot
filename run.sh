#!/bin/bash
DIR="$( cd "$( dirname "$0" )" && pwd )"
cd ${DIR}

PORTS=8008:5000
USER=root:root

CONTAINER_NAME=telegram_bot
NET=host

docker stop ${CONTAINER_NAME}
docker rm ${CONTAINER_NAME}
docker run \
    -d \
    -e TZ=Europe/Kiev \
    --restart always \
    --user ${USER} \
    --net ${NET} \
    --publish ${PORTS} \
    --name ${CONTAINER_NAME} \
    -v ${DIR}:/app \
    telegram_bot \
    python3 app.py
