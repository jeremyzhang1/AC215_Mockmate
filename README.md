AC215 (Milestone2)
==============================

AC215 - Milestone2

Project Organization
------------
```
.dvc/  
├─ .gitignore  
└─ config  
src/  
├─ api-frontend/  
│  └─ app/  
│     ├─ main.py  
│     └─ __init__.py  
├─ data-versioning/  
│  ├─ .gitignore  
│  ├─ cli.py  
│  ├─ docker-shell.sh  
│  ├─ Dockerfile  
│  ├─ leetcode_dataset_embeddings.dvc  
│  └─ requirements.txt  
└─ preprocessing/  
   ├─ .gitignore  
   ├─ docker-shell.sh
   ├─ Dockerfile  
   ├─ Pipfile  
   ├─ Pipfile.lock  
   └─ preprocess_cli.py  
.dvcignore  
.gitignore  
LICENSE  
README.md  
requirements.txt
```
--------
# AC215 - Milestone2 - Mockmate

**Team Members**  
Jeremy Zhang, Andrew Sima, Rudra Barua

**Group Name**  
Mockmate

**Project**  
In this project, our goal is to build an application that can simulate software engineering job interviews by generating technical questions relevant to the domain. This platform will also evaluate candidates' responses in real-time, offering feedback on coding efficiency and response quality.

### Milestone2 ###

In this milestone, we gathered data from [Leetcode](https://leetcode.com/problemset/all/), cleaned the data, versioned the data, and generated a rudimentary set of embeddings in support for training for the next milestone. We also devloped a set of atomic containers that runs each of the steps as well as a pipeline to push all the various pieces of processed data into GCP buckets.

**Preprocessing**


**Data Versioning**
