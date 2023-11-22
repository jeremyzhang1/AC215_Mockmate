#!/bin/bash

echo "Container is running!!!"

# this will run the api/service.py file with the instantiated app FastAPI
uvicorn_server() {
    pipenv run uvicorn api.main:app --host 0.0.0.0 --port 9000 --log-level debug --reload
}

uvicorn_server_production() {
    pipenv run uvicorn api.main:app --host 0.0.0.0 --port 9000 --lifespan on
}

export -f uvicorn_server
export -f uvicorn_server_production

echo -en "\033[92m
The following commands are available:
    uvicorn_server
        Run the Uvicorn Server
\033[0m
"

if [ "${DEV}" = 1 ]; then
  # Authenticate gcloud using service account
  gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
  # Set GCP Project Details
  gcloud config set project $GCP_PROJECT
  #/bin/bash
  pipenv shell
else
  # Authenticate gcloud using service account
  gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
  # Set GCP Project Details
  gcloud config set project $GCP_PROJECT
  # Get pkl file
  gcloud storage cp gs://mockmate-app-data/processed_leetcode_data/processed-leetcode.json /app/api
  # FastAPI server
  uvicorn_server
fi