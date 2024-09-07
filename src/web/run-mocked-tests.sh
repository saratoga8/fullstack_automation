#!/bin/bash

IMAGE_TAG=web

npm -v || exit 1
docker -v || exit 1

echo "Build Web App image..."
docker build -t "$IMAGE_TAG" . || exit 1
docker image inspect "$IMAGE_TAG" || exit 1

echo "Run Web App container"
docker run -p 3000:3000 --name web -d "$IMAGE_TAG:latest" || exit 1

echo "Run tests with mocked API"
npm i -D && npm run tests:mocked