#!/bin/bash

IMAGE_TAG=web
MOCK_IMAGE_TAG=mock

npm -v || exit 1
docker -v || exit 1

echo "Build Web App image..."
docker build -t "$IMAGE_TAG" . || exit 1
docker image inspect "$IMAGE_TAG" || exit 1

echo "Build the image of the Mock API server..."
docker build -t "$MOCK_IMAGE_TAG" -f ../api/Dockerfile.mock ../api || exit 1

echo "Run Web App container"
docker run -p 3000:3000 --name $IMAGE_TAG -d "$IMAGE_TAG:latest" || exit 1

echo "Run Mock API server"
docker run -p 8000:8000 --name $MOCK_IMAGE_TAG -d "$MOCK_IMAGE_TAG:latest" || exit 1

echo "Run tests with mocked API"
npm i -D && npm run tests:mocked
EXIT_CODE=$?

echo "Stopping containers..."
docker container stop $MOCK_IMAGE_TAG $IMAGE_TAG
echo "Delete containers..."
docker container rm $MOCK_IMAGE_TAG $IMAGE_TAG

exit $EXIT_CODE