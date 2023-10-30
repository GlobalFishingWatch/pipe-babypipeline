"""
Initialize datasets where to store the baby_pipeline results
1. Filter the datsets using labels, particularly the step:init_datasets (only created by baby_pipeline)
2. Remove the datsets but keep the last two dates.
"""
from google.cloud import bigquery as bq

import argparse
import logging
import re
import time

parser = argparse.ArgumentParser()
parser.add_argument('--dataset_prefix',
                    help='Pattern in babypipeline datasets which has the date on it. Date Format: str.',
                    default="pipe_ais_test_YYYYMMDD",
                    required=False)
required = parser.add_argument_group('Required named arguments')

def get_pipe_ver():
    with open('setup.py') as rf:
        return re.search(r'version=\'(v[0-9.]*)\'', rf.read()).group(1)

def prune_datasets(argv):
    """
    Prune the baby pipeline datasets where was stored the baby_pipeline results
    """
    options = parser.parse_args(argv)
    start_time = time.time()

    logging.info(f'Removal of baby-pipeline datasets version {get_pipe_ver()}')
    logging.info('Running prune baby pipeline datasets with args %s', options)
    client = bq.Client()
    PATTERN_LEN = len(options.dataset_prefix)

    get_datasets = client.list_datasets(filter='labels.step:init_datasets') # Make an API request.
    if not get_datasets:
        logging.info(f'Baby-pipeline datasets to remove not found.')
        return 0
    datasets = list(map(lambda x: x.dataset_id, get_datasets))

    dataset_pattern_uniques = list(set(map(lambda x:x[:PATTERN_LEN], datasets)))
    dataset_pattern_uniques.sort()
    pattern_to_remove = dataset_pattern_uniques[:-2]

    datasets_to_remove = list(filter(lambda x: x[:PATTERN_LEN] in pattern_to_remove, datasets))
    for dataset_id in datasets_to_remove:
        client.delete_dataset(
            dataset_id, delete_contents=True, not_found_ok=True
        ) # Make an API request.

    ### ALL DONE
    logging.info(f'Baby-pipeline datasets removed: {datasets_to_remove}')
    logging.info(f'Execution time {(time.time()-start_time)/60} minutes')
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(prune_datasets(sys.argv[1:]))
