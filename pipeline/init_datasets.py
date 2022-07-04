"""
Initialize datasets where to store the baby_pipeline results
1. Stores the dataset_moment to GCS
2. Create the datasets in case they don't exists.
"""
from google.api_core.exceptions import NotFound
from google.cloud import bigquery as bq
from google.cloud import storage as st

import argparse
import datetime as dt
import logging
import re
import time


DATASET_PREFIX='pipe_ais_test_'

parser = argparse.ArgumentParser()
parser.add_argument('--project',
                    help='Project identification. Format: str.',
                    required=True)
parser.add_argument('--dataset_suffixes',
                    help='Datasets suffixes separated by comma. Format: str.',
                    required=True)
parser.add_argument('--storepath',
                    help='Google Cloud Storage path where to store the moment. Format: str.',
                    default='gs://ais-gfw/baby_pipeline/dataset_moment.txt',
                    required=False)
parser.add_argument('--location',
                    help='Dataset location. Format: str.',
                    default='US',
                    required=False)


def save_moment_gcs(options, ds_moment: str):
    """
    Saves the dataset prefix with the momento in the GCS.
    Ex. pipe_ais_test_20220701100000. Useful for baby_pipeline datasets."""

    path = re.search('gs://([^/]*)/(.*)', options.storepath)
    bucket_name = path.group(1)
    destination_blob_name = path.group(2)

    client = st.Client(options.project)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(ds_moment)

    logging.info(
        f'{destination_blob_name} with content {ds_moment} uploaded to {bucket_name}.'
    )



def initialize(argv):
    """
    Initialize datasets where to store the baby_pipeline results
    1. Stores the dataset_moment to GCS
    2. Create the datasets in case they don't exists.
    """
    options = parser.parse_args(argv)

    start_time = time.time()

    logging.info('Running initialize baby pipeline datasets with args %s', options)
    client = bq.Client(options.project)


    ds_moment = f'{DATASET_PREFIX}{dt.datetime.now().strftime("%Y%m%d%H%M%S")}'
    save_moment_gcs(options, ds_moment)

    complete_ds = [f'{ds_moment}_{dataset_suffix}' for dataset_suffix in options.dataset_suffixes.split(',')]
    logging.info(f'Datasets proposed {complete_ds}', )

    for dataset_id in complete_ds:
        try:
            # First check if datasets already exists
            ds_exists = client.get_dataset(dataset_id)  # Make an API request.
            logging.warn(f'Dataset {ds_exists} already exists.')
        except NotFound:
            #if not found, create it
           ds = bq.Dataset(f'{options.project}.{dataset_id}') # Full dataset obj to send to API
           ds.location = options.location
           ds = client.create_dataset(ds, timeout=30) # Make an API request
           logging.info(f'Created dataset {options.project}.{ds.dataset_id}')

    ### ALL DONE
    logging.info('All done, you can find the output file here: {0}'.format(options.storepath))
    logging.info('Execution time {0} minutes'.format((time.time()-start_time)/60))

if __name__ == '__main__':
    import sys
    initialize(sys.argv[1:])
