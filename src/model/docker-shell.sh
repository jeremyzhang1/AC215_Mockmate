#!/bin/bash

set -e
export BASE_DIR="$(pwd)"
export SECRETS_DIR="$(pwd)"/../secrets/
export GCS_BUCKET_NAME="mockmate-app-data"
export GCP_PROJECT="mockmate"
export GCP_ZONE="us-central1-a"

# Create the network if we don't have it yet
docker network inspect model-train-serve-network >/dev/null 2>&1 || docker network create model-train-serve-network

# Build the image based on the Dockerfile
# docker build -t model-train-serve-cli --platform=linux/arm64/v8 -f Dockerfile .
docker build -t model-train-serve-cli -f Dockerfile .

# Run Container
docker run --rm --name model-train-serve-cli -ti \
--gpus all \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-v ~/.gitconfig:/etc/gitconfig \
-e GOOGLE_APPLICATION_CREDENTIALS=/secrets/data-service-account.json \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCP_ZONE=$GCP_ZONE \
-e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
--network model-train-serve-network model-train-serve-cli
