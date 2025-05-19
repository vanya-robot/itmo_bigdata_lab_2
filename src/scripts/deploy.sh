#!/bin/bash
set -e

if [ -z "$DOCKERHUB_USERNAME" ] || [ -z "$DOCKERHUB_TOKEN" ]; then
  echo "ERROR: Docker credentials not set!"
  exit 1
fi

VERSION=$(git describe --tags --always || echo "latest")
TIMESTAMP=$(date +%Y%m%d%H%M%S)

echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin

docker build -t $DOCKERHUB_USERNAME/penguin-classifier-withDB:latest \
             -t $DOCKERHUB_USERNAME/penguin-classifier-withDB:$VERSION \
             -t $DOCKERHUB_USERNAME/penguin-classifier-withDB:$TIMESTAMP .

docker push $DOCKERHUB_USERNAME/penguin-classifier-withDB --all-tags