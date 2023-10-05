# this script is not so useful anymore, since we can just directly pull from huggingface

# figure out how we actually pull from dvc though

import argparse
from transformers import AutoTokenizer

model_name = "tiiuae/falcon-7b"  # hardcode the model name for now
model_dir_name = "falcon7b"


def pull_initial_model_to_local():
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.save_pretrained(f"model_store/{model_dir_name}")


def pull_versioned_model_from_dvc():
    pass


def main(args=None):
    if args.init:
        pull_initial_model_to_local()
    else:
        pull_versioned_model_from_dvc()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Model Loader CLI...")
    parser.add_argument(
        "-i",
        "--init",
        action="store_true",
        help="Pull the initial model to local",
    )
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
