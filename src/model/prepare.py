import os
import json
import pickle
import shutil
import time

import dask
import dask.bag as db
from dask.distributed import Client
from google.cloud import storage


# generic function to first download data from bucket
def parse_leetcode_data(bucket_name):
    print("downloading processed leetcode data")

    # init storage client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix="processed_leetcode_data/")

    # download annotations
    for blob in blobs:
        print("Annotation file:", blob.name)

        if not blob.name.endswith("processed_leetcode_data/"):
            with blob.open("r") as f:
                return json.load(f)


# the format that we want is the Alpaca format
@dask.delayed
def transform_to_alpaca_ddelayed_format(entry):
    preamble = """Below is an instruction that describes a coding task, along with given constraints and examples of test cases that you are required to pass.
    Write a solution that appropriately solves the coding task using python code and an explanation for your code."""
    stitched_prompt = (
        preamble
        + "\n### Instruction: "
        + str(entry["question"])
        + "\n### Constraints: "
        + entry["constraints"]
        + "\n### Examples: "
        + "\n".join(entry["examples"])
        + "\n### Solution and Explanation: "
    )
    expected_response = (
        "### Solution: "
        + entry["python_sol"]
        + "\n### Explanation: "
        + entry["explanation"]
    )
    return {"prompt": stitched_prompt, "response": expected_response}


def clean_entry(entry):
    for key in ["question", "constraints", "examples", "python_sol", "explanation"]:
        if key not in entry or entry[key] is None:
            return False
    return True


# script used to prepare the training data using Dask
if __name__ == "__main__":
    dataset_result_folder = "training_data"
    bucket_name = os.environ["GCS_BUCKET_NAME"]

    # init the parallel processing cluster with 4 Dask workers
    cluster = Client()
    dask.config.set(num_workers=4)

    # pull leetcode data
    leetcode_list = parse_leetcode_data(bucket_name)

    # clean code in parallel
    b = db.from_sequence(leetcode_list)
    cleaned_leetcode_list = list(b.filter(clean_entry))

    # get delayed compute list
    lazy_leetcode_training_data = [
        transform_to_alpaca_ddelayed_format(entry) for entry in cleaned_leetcode_list
    ]

    start = time.time()
    lazy_leetcode_training_data = dask.compute(lazy_leetcode_training_data)

    # print results and save to local file
    print("dask computation time:", time.time() - start)
    shutil.rmtree(dataset_result_folder, ignore_errors=True, onerror=None)
    os.makedirs(dataset_result_folder, exist_ok=True)

    with open(dataset_result_folder + "/ready.pkl", "wb") as handle:
        pickle.dump(
            lazy_leetcode_training_data,
            handle,
            protocol=pickle.HIGHEST_PROTOCOL,
        )
