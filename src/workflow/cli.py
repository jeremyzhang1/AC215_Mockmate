"""
Module that contains the command line app.

Typical usage example from command line:
        python cli.py
"""

import os
import argparse
import random
import string
from kfp import dsl
from kfp import compiler
import google.cloud.aiplatform as aip
# from model import model_training, model_deploy


GCP_PROJECT = "mockmate-400103"
GCS_BUCKET_NAME = "mockmate-app-data"
BUCKET_URI = f"gs://{GCS_BUCKET_NAME}"
PIPELINE_ROOT = f"{BUCKET_URI}/pipeline_root/root"
GCS_SERVICE_ACCOUNT = "ml-workflow@mockmate-400103.iam.gserviceaccount.com"
# GCS_PACKAGE_URI = os.environ["GCS_PACKAGE_URI"]
# GCP_REGION = os.environ["GCP_REGION"]

DATA_PREPROCESSING_IMAGE = "docker.io/zhangjeremy1/mockmate-data-preprocess:latest"
DATA_VERSIONING_IMAGE = "docker.io/zhangjeremy1/data-version-cli:latest"
MODEL_IMAGE = "docker.io/zhangjeremy1/model-train-serve-cli:latest"

BASE_DIR = os.getcwd()
SECRETS_DIR = os.getcwd() + "/../secrets"
GOOGLE_APPLICATION_CREDENTIALS= "/secrets/data-service-account.json"


def generate_uuid(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def main(args=None):
    print("CLI Arguments:", args)

    if args.data_preprocessor:
        print("data preprocessor")
        
        # Define a container component for each step of data preprocessor
        @dsl.container_component
        def data_preprocessor_download():
            container_spec = dsl.ContainerSpec(
                image=DATA_PREPROCESSING_IMAGE,
                command=[],
                args=[
                    "preprocess_cli.py",
                    "-d",
                ]
            )
            return container_spec

        @dsl.container_component
        def data_preprocessor_clean():
            container_spec = dsl.ContainerSpec(
                image=DATA_PREPROCESSING_IMAGE,
                command=[],
                args=[
                    "preprocess_cli.py",
                    "-c",
                ]
            )
            return container_spec

        @dsl.container_component
        def data_preprocessor_upload():
            container_spec = dsl.ContainerSpec(
                image=DATA_PREPROCESSING_IMAGE,
                command=[],
                args=[
                    "preprocess_cli.py",
                    "-u",
                ]
            )
            return container_spec

        # Define a pipeline
        @dsl.pipeline
        def data_preprocessor_pipeline():
            data_download_task = data_preprocessor_download().set_display_name("Data Download")
            data_clean_task = (
                data_preprocessor_clean()
                .set_display_name("Data Clean")
                .after(data_download_task)
            )
            data_upload_task = (
                data_preprocessor_upload()
                .set_display_name("Data Upload")
                .after(data_clean_task)
            )

        # Build yaml file for pipeline
        compiler.Compiler().compile(
            data_preprocessor_pipeline, package_path="data_preprocessor.yaml"
        )

        # Submit job to Vertex AI
        aip.init(project=GCP_PROJECT, staging_bucket=BUCKET_URI)

        job_id = generate_uuid()
        DISPLAY_NAME = "mockmate-data-preprocessing-" + job_id
        job = aip.PipelineJob(
            display_name=DISPLAY_NAME,
            template_path="data_preprocessor.yaml",
            pipeline_root=PIPELINE_ROOT,
            enable_caching=False,
        )

        job.run(service_account=GCS_SERVICE_ACCOUNT)

    if args.data_versioning:
        print("data versioning/embedding generation")
        
        # Define a container component for each step of data versioning/embeddings
        @dsl.container_component
        def data_embeddings():
            container_spec = dsl.ContainerSpec(
                image=DATA_VERSIONING_IMAGE,
                command=[],
                args=[
                    "cli.py",
                    "-d",
                    "-c 100",
                ]
            )
            return container_spec
        
        # Define a pipeline
        @dsl.pipeline
        def data_embeddings_pipeline():
            data_embeddings()

        # Build yaml file for pipeline
        compiler.Compiler().compile(
            data_embeddings_pipeline, package_path="data_embeddings.yaml"
        )

        # Submit job to Vertex AI
        aip.init(project=GCP_PROJECT, staging_bucket=BUCKET_URI)

        job_id = generate_uuid()
        DISPLAY_NAME = "mockmate-data-embeddings-" + job_id
        job = aip.PipelineJob(
            display_name=DISPLAY_NAME,
            template_path="data_embeddings.yaml",
            pipeline_root=PIPELINE_ROOT,
            enable_caching=False,
        )

        job.run(service_account=GCS_SERVICE_ACCOUNT)

    if args.model_tuning:
        print("fine tuning")
        
        # Define a container component for each step of model training and deployment
        @dsl.container_component
        def prepare_data():
            container_spec = dsl.ContainerSpec(
                image=MODEL_IMAGE,
                command=[],
                args=[
                    "prepare.py",
                ]
            )
            return container_spec
        
        @dsl.container_component
        def load_model():
            container_spec = dsl.ContainerSpec(
                image=MODEL_IMAGE,
                command=[],
                args=[
                    "loader.py",
                    "-p",
                ]
            )
            return container_spec
        
        @dsl.container_component
        def finetune():
            container_spec = dsl.ContainerSpec(
                image=MODEL_IMAGE,
                command=[],
                args=[
                    "finetune.py",
                ]
            )
            return container_spec
        
        @dsl.container_component
        def serve_query():
            container_spec = dsl.ContainerSpec(
                image=MODEL_IMAGE,
                command=[],
                args=[
                    "query.py",
                ]
            )
            return container_spec
        
        # Define a pipeline
        @dsl.pipeline
        def model_pipeline():
            prepare_data_task = prepare_data().set_display_name("Prepare Data")
            load_model_task = (
                load_model()
                .set_display_name("Load Model")
                .after(prepare_data_task)
            )
            fine_tune_task = (
                finetune()
                .set_display_name("Fine Tune Model")
                .after(load_model_task)
            )
            serve_query_task = (
                serve_query()
                .set_display_name("Serve Query Task")
                .after(fine_tune_task)
            )

        # Build yaml file for pipeline
        compiler.Compiler().compile(
            model_pipeline, package_path="model_pipeline.yaml"
        )

        # Submit job to Vertex AI
        aip.init(project=GCP_PROJECT, staging_bucket=BUCKET_URI)

        job_id = generate_uuid()
        DISPLAY_NAME = "mockmate-model-tuning-" + job_id
        job = aip.PipelineJob(
            display_name=DISPLAY_NAME,
            template_path="model_pipeline.yaml",
            pipeline_root=PIPELINE_ROOT,
            enable_caching=False,
        )

        job.run(service_account=GCS_SERVICE_ACCOUNT)
    
    # if args.everything:
    #     print("full pipeline")
    #     pass

if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(description="Workflow CLI")

    parser.add_argument(
        "-d",
        "--data_preprocessor",
        action="store_true",
        help="Run just the Data Preprocessing",
    )
    parser.add_argument(
        "-v",
        "--data_versioning",
        action="store_true",
        help="Run just the Data Versioning",
    )
    parser.add_argument(
        "-m",
        "--model_tuning",
        action="store_true",
        help="Run just Model Tuning",
    )
    parser.add_argument(
        "-e",
        "--everything",
        action="store_true",
        help="Run all steps of pipeline",
    )

    args = parser.parse_args()

    main(args)
