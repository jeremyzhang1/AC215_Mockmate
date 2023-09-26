"""
Module that contains the command line app.
"""
import argparse
import os
import traceback
import time
from google.cloud import storage
import shutil
import glob
import json


GCS_BUCKET_NAME = os.environ["GCS_BUCKET_NAME"]


def make_local_dataset_folders(dataset_prep_folder):
    print("cleaning and remaking local dataset folders")
    
    shutil.rmtree(dataset_prep_folder, ignore_errors=True, onerror=None)
    os.makedirs(dataset_prep_folder, exist_ok=True)
    dataset_folder = "leetcode_dataset"
    shutil.rmtree(dataset_folder, ignore_errors=True, onerror=None)
    os.makedirs(dataset_folder, exist_ok=True)


def download_processed_leetcode_data(bucket_name, dataset_prep_folder):
    print("downloading processed leetcode data")
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix="processed_leetcode_data/")

    # Download annotations
    for blob in blobs:
        print("Annotation file:", blob.name)

        if not blob.name.endswith("processed_leetcode_data/"):
            filename = os.path.basename(blob.name)
            local_file_path = os.path.join(dataset_prep_folder, filename)
            blob.download_to_filename(local_file_path)


def download_data():
    print("download_data")

    bucket_name = GCS_BUCKET_NAME
    dataset_prep_folder = "leetcode_dataset_prep"

    print("bucket_name:", bucket_name,
          "dataset_prep_folder:", dataset_prep_folder)

    # Clear dataset folders
    make_local_dataset_folders(dataset_prep_folder)

    # Initiate Storage client and download processed leetcode data
    download_processed_leetcode_data(bucket_name, dataset_prep_folder)

    # Organize annotation with images
    annotation_files = glob.glob(os.path.join(dataset_prep_folder, "*"))
    for annotation_file in annotation_files:
        # Read the json file
        with open(annotation_file, "r") as read_file:
            annotation_json = json.load(read_file)

        # Annotations
        # annotations = annotation_json["annotations"]
        # Assume we pick just the first annotation from the labeled list
        if len(annotation_json["result"]) > 0:
            label = annotation_json["result"][0]["value"]["choices"][0]
            # Create the label folder
            label_folder = os.path.join(dataset_folder, label)
            os.makedirs(label_folder, exist_ok=True)

            # Download the image from GCS [Another option could be to just store the image url and label in DVC]
            image_url = annotation_json["task"]["data"]["image"]
            image_url = image_url.replace("gs://", "").replace(
                GCS_BUCKET_NAME + "/", ""
            )
            print("image_url:", image_url)
            blob = bucket.blob(image_url)
            filename = os.path.basename(blob.name)
            local_file_path = os.path.join(label_folder, filename)
            blob.download_to_filename(local_file_path)


def main(args=None):
    if args.download:
        download_data()


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(description="Data Versioning CLI...")

    parser.add_argument(
        "-d",
        "--download",
        action="store_true",
        help="Download labeled data from a GCS Bucket",
    )

    args = parser.parse_args()

    main(args)
