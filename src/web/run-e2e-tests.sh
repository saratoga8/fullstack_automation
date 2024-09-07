#!/bin/bash

WORK_PATH=$PWD

npm -v || exit 1
docker -v || exit 1

echo "Build API server image..."
cd ../api && docker build -t api . || exit 1
docker image inspect api || exit 1

cd "$WORK_PATH"
echo "Build Web App image..."
docker build -t web . || exit 1
docker image inspect web || exit 1

echo "Running composition..."
docker-compose up -d

echo "Running E2E tests..."
npm i -D && npm run e2e