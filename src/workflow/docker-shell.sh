#!/bin/bash

set -e

export IMAGE_NAME="mockmate-workflow"
export BASE_DIR="$(pwd)"
export SECRETS_DIR="$(pwd)"/../secrets/
export GCP_PROJECT="ac215-project"
export GCS_BUCKET_NAME="mockmate-app-data"
export GCS_SERVICE_ACCOUNT="ml-workflow@mockmate-400103.iam.gserviceaccount.com"
export GCP_REGION="us-central1"

# Build the image based on the Dockerfile
docker build -t $IMAGE_NAME -f Dockerfile .
# docker build -t $IMAGE_NAME --platform=linux/amd64 -f Dockerfile .


# Run Container
docker run --rm --name $IMAGE_NAME -ti \
-v "$SECRETS_DIR":/secrets \
-e GOOGLE_APPLICATION_CREDENTIALS=/secrets/ml-workflow.json \
--mount type=bind,source="$BASE_DIR",target=/app $IMAGE_NAME
# -e GCP_PROJECT=$GCP_PROJECT \
# -e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
# -e GCS_SERVICE_ACCOUNT=$GCS_SERVICE_ACCOUNT \
# -e GCP_REGION=$GCP_REGION \
# $IMAGE_NAME
