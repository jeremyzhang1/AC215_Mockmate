"""
Module that contains the command line app.
"""
import os
import argparse
import shutil
import json
import re
from google.cloud import storage

# Generate the inputs arguments parser
parser = argparse.ArgumentParser(description="Command description.")

gcp_project = "mockmate"
bucket_name = "mockmate-app-data"
unprocessed_leetcode = "unprocessed_leetcode_data"
processed_leetcode = "processed_leetcode_data"


def makedirs():
    os.makedirs(unprocessed_leetcode, exist_ok=True)
    os.makedirs(processed_leetcode, exist_ok=True)


def download_unprocessed():
    print("Downloading unprocessed LeetCode data")

    # Clear
    shutil.rmtree(unprocessed_leetcode, ignore_errors=True, onerror=None)
    makedirs()

    storage_client = storage.Client(project=gcp_project)

    bucket = storage_client.bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=f"{unprocessed_leetcode}/")
    for blob in blobs:
        if blob.name.endswith(".jsonl"):
            print(blob.name)
            blob.download_to_filename(blob.name)

def clean_data():
    print("Cleaning LeetCode dataset")
    makedirs()

    entries = []

    # List all files in the unprocessed data directory
    data_files = os.listdir(unprocessed_leetcode)

    for filename in data_files:
        full_path = os.path.join(unprocessed_leetcode, filename)
        with open(full_path, "r") as file:
            for line in file:
                if line:  # Check if line is not empty
                    entries.append(json.loads(line))

    processed_entries = []

    for entry in entries:
        id = entry.get('id', None)
        slug = entry.get('slug', None)
        difficulty = entry.get('difficulty', None)

        answers = entry.get('answer', {})  # default to an empty dictionary if 'answer' isn't present
        cpp_sol = answers.get('c++', None)
        java_sol = answers.get('java', None)
        py_sol = answers.get('python', None)
        js_sol = answers.get('javascript', None)
        sol_exp = answers.get('explanation', None)

        text = entry.get('content', None)

        # Extract the question as everything before the first "Example"
        question_pattern = r"^(.*?)(?:\*\*Example \d+:|$)"
        question_match = re.search(question_pattern, text, re.DOTALL)
        question = question_match.group(1).strip() if question_match else None

        # Extract individual examples
        examples_pattern = r"(\*\*Example \d+:.*?)(?=\*\*Example \d+:|\*\*Constraints:|$)"
        examples_matches = re.findall(examples_pattern, text, re.DOTALL)
        examples = [match.strip() for match in examples_matches]

        # Extract constraints
        # Extract constraints
        constraints_pattern = r"(?<=\*\*Constraints:\*\*\s)(.*?)(?=\s*\*\*Follow-up:|$)"
        constraints_match = re.search(constraints_pattern, text, re.DOTALL)
        constraints = constraints_match.group(0).strip() if constraints_match else None

        # Extract follow-up
        followup_pattern = r"(?<=\*\*Follow-up:\*\* ).*"
        followup_match = re.search(followup_pattern, text)
        followup = followup_match.group(0).strip() if followup_match else None

        # Print the extracted parts
        # print("Question:")
        # print(question)
        # print("\n" + "-"*50 + "\n")

        # for example in examples:
        #     print("Example:")
        #     print(example)
        #     print("\n" + "-"*50 + "\n")

        # print("Constraints:")
        # print(constraints)
        # print("\n" + "-"*50 + "\n")

        # print("Follow-up:")
        # print(followup)
        
        # Form a dictionary with the extracted data
        processed_entry = {
            "id": id,
            "slug": slug,
            "difficulty": difficulty, 
            "cpp_sol": cpp_sol,
            "java_sol": java_sol,
            "python_sol": py_sol,
            "javascript_sol": js_sol,
            "explanation": sol_exp,
            "question": question,
            "examples": examples,
            "constraints": constraints,
            "followup": followup
        }

        processed_entries.append(processed_entry)


    # Write the list of dictionaries as a single JSON object
    with open(f"{processed_leetcode}/processed-leetcode.json", "w") as outfile:
        json.dump(processed_entries, outfile, indent=2, default = lambda x: x.__dict__)

def upload_processed():
    print("Uploading processed LeetCode data")
    makedirs()

    # Upload to bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Get the list of text file
    data_files = os.listdir(processed_leetcode)

    for json_file in data_files:
        file_path = os.path.join(processed_leetcode, json_file)

        destination_blob_name = file_path
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(file_path)

def main(args=None):
    print("Args:", args)

    if args.download:
        download_unprocessed()
    if args.clean:
        clean_data()
    if args.upload:
        upload_processed()


if __name__ == "__main__":
    # Generate the inputs arguments parser
    parser = argparse.ArgumentParser(description="Preprocessing for MockMate LeetCode data")

    parser.add_argument(
        "-d",
        "--download",
        action="store_true",
        help="Download unproccessed LeetCode data from GCS bucket",
    )

    parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="Process and clean the LeetCode data",
    )

    parser.add_argument(
        "-u",
        "--upload",
        action="store_true",
        help="Upload cleaned LeetCode data to GCS bucket",
    )

    args = parser.parse_args()

    main(args)
    