#!/bin/bash

open --background -a Docker

wait_for_docker_start() {
  while ! docker info >/dev/null 2>&1; do
    echo "Waiting for Docker to start..."
    sleep 2
  done
  echo "Docker is running!"
}

wait_for_docker_start

docker-compose build

docker-compose up -d


