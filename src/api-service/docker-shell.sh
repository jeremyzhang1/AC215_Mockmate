#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Define some environment variables
export IMAGE_NAME="mockmate-api-backend"
export BASE_DIR="$(pwd)"
export SECRETS_DIR="$(pwd)"/../secrets/
export GCP_PROJECT="mockmate-400103"
export ENDPOINT_ID="6050992918674538496"
export REGION="us-central1"

# Build the image based on the Dockerfile
# docker build -t $IMAGE_NAME -f Dockerfile .

# Run the container
docker run --rm --name $IMAGE_NAME -ti \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-p 9000:9000 \
-e GOOGLE_APPLICATION_CREDENTIALS=/secrets/mockmate-mlservice.json \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
-e ENDPOINT_ID=$ENDPOINT_ID \
-e REGION=$REGION \
$IMAGE_NAME
