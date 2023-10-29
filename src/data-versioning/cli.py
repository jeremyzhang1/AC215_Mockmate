"""
Module that contains the command line app.
"""
import argparse
import glob
import json
import os
import pickle
import shutil

from google.cloud import storage
from sentence_transformers import SentenceTransformer


def make_local_dataset_folders(dataset_prep_folder, dataset_result_folder):
    print("cleaning and remaking local dataset folders")
    
    shutil.rmtree(dataset_prep_folder, ignore_errors=True, onerror=None)
    os.makedirs(dataset_prep_folder, exist_ok=True)
    shutil.rmtree(dataset_result_folder, ignore_errors=True, onerror=None)
    os.makedirs(dataset_result_folder, exist_ok=True)


def download_processed_leetcode_data(bucket_name, dataset_prep_folder):
    print("downloading processed leetcode data")

    # init storage client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix="processed_leetcode_data/")

    # download annotations
    for blob in blobs:
        print("Annotation file:", blob.name)

        if not blob.name.endswith("processed_leetcode_data/"):
            filename = os.path.basename(blob.name)
            local_file_path = os.path.join(dataset_prep_folder, filename)
            blob.download_to_filename(local_file_path)


def create_and_save_vector_embeddings(file, count):
    # read the json file
    with open(file, "r") as read_file:
        leetcode_json = json.load(read_file)

        print("process json of length", len(leetcode_json), "from file", file)

        problems = []
        solutions = []

        for problem in leetcode_json[:count]:
            problem_dict = {key: problem[key] for key in [
                "id",
                "slug",
                "difficulty",
                "question",
                "examples",
                "constraints",
                "followup"
            ]}
            solution_dict = {key: problem[key] for key in [
                "id",
                "cpp_sol",
                "java_sol",
                "python_sol",
                "javascript_sol",
                "explanation",
            ]}
            problem_embedding = embedding_model.encode(
                json.dumps(problem_dict)
            )
            solution_embedding = embedding_model.encode(
                json.dumps(solution_dict)
            )

            problems.append(problem_embedding)
            solutions.append(solution_embedding)

        print("finished generating problem and solution embeddings")

        with open(dataset_result_folder + '/problems.pkl', 'wb') as handle:
            pickle.dump(problems,
                        handle,
                        protocol=pickle.HIGHEST_PROTOCOL)
            
        with open(dataset_result_folder + '/solutions.pkl', 'wb') as handle:
            pickle.dump(solutions,
                        handle,
                        protocol=pickle.HIGHEST_PROTOCOL)


def download_data(count):
    # clear dataset folders
    make_local_dataset_folders(dataset_prep_folder, dataset_result_folder)

    # initiate Storage client and download processed leetcode data
    download_processed_leetcode_data(bucket_name, dataset_prep_folder)

    # organize annotation with images
    annotation_files = glob.glob(os.path.join(dataset_prep_folder, "*"))
    for annotation_file in annotation_files:
        create_and_save_vector_embeddings(annotation_file, count)
        

def main(args=None):
    if args.download:
        download_data(args.count)


if __name__ == "__main__":
    # init environment objects
    bucket_name = os.environ["GCS_BUCKET_NAME"]
    dataset_prep_folder = "leetcode_dataset_prep"
    dataset_result_folder = "leetcode_dataset_embeddings"
    print("bucket_name:", bucket_name,
          "dataset_prep_folder:", dataset_prep_folder)

    # init model object
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    # generate the inputs arguments parser
    # if you type 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(description="Data Versioning CLI...")

    parser.add_argument(
        "-d",
        "--download",
        action="store_true",
        help="Download labeled data from a GCS Bucket",
    )

    parser.add_argument(
        "-c",
        "--count",
        type=int,
        help="number of problems to generate vector embeddings for",
    )

    args = parser.parse_args()

    main(args)
