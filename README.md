# pipe-babypipeline

## Introduction

This pipeline handles all related stuff that the baby_pipeline needs to be active.

## Prerequisites

We use a dockerized development environment, so you will need [docker](https://www.docker.com/)  and [docker-compose](https://docs.docker.com/compose/) on your machine. We also need the authorization files that will be used to authorize access to google cloud services. No other dependencies are required in your machine.

To setup google cloud sdk authorization, follow these steps:

* Configure docker to use google cloud to authorize access to our base images by running `gcloud auth configure-docker`.

* Create a docker volume named `gcp` to store the google cloud credentials that docker will use by running `docker volume create --name gcp`. This volume will be shared by all your pipeline repositories, so you need to run this only once.

* Setup GCP authorization inside docker by running `docker-compose run --rm gcloud --project=world-fishing-827 auth application-default login` and following the instructions.


## Repository structure

The following are important files and folders in the repository:

* `requirements-scheduler.txt`: List of pinned dependencies that the project needs to run. These dependencies are automatically installed when you run `docker-compose build`.
* `main.py`: This is the application entry point.
* `pipeline/`: This folder contains the python modules that the baby pipeline needs.

### How to run
To run in docker:
```console
docker compose run --rm dev
```
Note that the first time you do this, docker will build the image for you.

## what it does?

* `init_datasets`: Initialize datasets where to store the baby_pipeline results. Creates the datasets in case they don't exists.

