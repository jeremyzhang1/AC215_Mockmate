import argparse
import os
import shutil
import dvc.api


# TODO: rudra.barua figure out how to actually download models from DVC
def pull_versioned_model_from_dvc(model_data_folder):
    # remove and recreate the model_data folder
    shutil.rmtree(model_data_folder, ignore_errors=True, onerror=None)
    os.makedirs(model_data_folder, exist_ok=True)

    # we will always just pull the most up to date version for now
    dvc.api.read(
        'model.pkl',
        repo='https://github.com/iterative/example-get-started'
        mode='rb'
    )


def main(args=None):
    if args.pull:
        model_data = "trained_model"
        pull_versioned_model_from_dvc(model_data)


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
