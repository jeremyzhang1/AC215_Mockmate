# Instructions for Running Leetcode Data Processing Pipeline

## Preprocessing

This is the pre-processing container for downloading, cleaning, and re-uploading the raw leetcode data that we collected to our GCP bucket. The first step is to get the Docker container up and running:

```
./docker-shell.sh
```

Once inside the container, to download, run:

```
python preprocess_cli.py -d
```

Then to clean, run:

```
python preprocess_cli.py -c
```

and finally to upload the cleaned data run:


```
python preprocess_cli.py -u
```

## Data Versioning

This is the post processing container for generating vector embeddings off of the cleaned leetcode data from the preprocessing container. Similar to the above section, first get into the Docker container.

```
./docker-shell.sh
```

Once inside the docker container, we can run:

```
python cli.py -d -c 100 # the count arg specifies for how many problems we want to generate vector embeddings
```

Keep in mind that it takes around 30-40s to generate an embedding for a given leetcode problem, with there being ~2360 leetcode problems in entire dataset.

### Push data to DVC

The vector embeddings that we have are saved to the leetcode_dataset_embeddings folder. To reupload the data, make sure that you have the google cloud credentials correctly configured. You can do this via something similar to the following command (make sure to run in dvc root). 

```
dvc remote modify --local src/data-versioning/leetcode_dataset_embeddings \
                    credentialpath '<your secrets path>'
```

Then to update dvc for newly generated embeddings, run:

```
dvc add src/data-versioning/leetcode_dataset_embeddings

dvc push 
```