#! /usr/bin/env python3

import argparse
import os

import yaml

from pbs_sentient_exporter import PbsServer, get_backup_metrics

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export metrics for Proxmox Backup Server to Prometheus")
    parser.add_argument("-c", "--config", default=os.environ.get("PBS_SENTIENT_EXPORTER_CONFIG", "./config.yml"))
    args = parser.parse_args()

    with open(args.config, "r") as file:
        config = yaml.safe_load(file)

    pbs = PbsServer(**config)

    for m in get_backup_metrics(pbs):
        print(m)
