#! /usr/bin/env python
import sys
import logging

from pipeline.init_datasets import initialize as run_init_datasets

logging.basicConfig(level=logging.INFO)

SUBCOMMANDS = {
    "init_datasets": run_init_datasets,
}

if __name__ == "__main__":
    logging.info("Running %s", sys.argv)

    if len(sys.argv) < 2:
        logging.info("No subcommand specified. Run pipeline [SUBCOMMAND], where subcommand is one of %s", SUBCOMMANDS.keys())
        exit(1)

    subcommand = sys.argv[1]
    subcommand_args = sys.argv[2:]

    SUBCOMMANDS[subcommand](subcommand_args)
