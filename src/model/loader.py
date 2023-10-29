import argparse
import os
import shutil
import dvc.api

def pull_versioned_model_from_dvc(model_data_folder, rev=None):
    """
    Pull all pkl files from the DVC remote to the specified local folder.
    
    Args:
    - model_data_folder (str): Local directory to save the pulled files.
    - rev (str, optional): Specific version (git commit/branch/tag) of the data to pull. 
                            If None, it will pull the latest version.
    """

    # Remove and recreate the model_data folder
    shutil.rmtree(model_data_folder, ignore_errors=True, onerror=None)
    os.makedirs(model_data_folder, exist_ok=True)

    # Using DVC's open function to iterate and pull files
    with dvc.api.open(
        path='src/model/training_data/',
        mode='rb',
        remote='src/data-versioning/leetcode_dataset_embeddings',
        rev=rev
    ) as fd:
        for file in fd:
            if file.endswith('.pkl'):
                dst = os.path.join(model_data_folder, os.path.basename(file))
                with open(dst, 'wb') as out_file:
                    out_file.write(fd.read())

def main(args=None):
    if args.pull:
        model_data = "trained_model"
        pull_versioned_model_from_dvc(model_data, rev=args.version)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Model Loader CLI...")
    parser.add_argument(
        "-p",
        "--pull",
        action="store_true",
        help="Pull the versioned model from dvc",
    )
    parser.add_argument(
        "-v",
        "--version",
        type=str,
        help="Version of the model",
    )

    args = parser.parse_args()
    main(args)
