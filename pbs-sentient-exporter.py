#! /usr/bin/env python3

import argparse
import os
from time import sleep

from pbs_sentient_exporter import (PbsCollector, PbsServer, load_config,
                                   start_http_server)

DEFAULT_CONFIG_PATH = "/etc/pbs-sentient-exporter/config.yml"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export metrics for Proxmox Backup Server to Prometheus")
    parser.add_argument("-c", "--config", default=os.environ.get("PBS_SENTIENT_EXPORTER_CONFIG", DEFAULT_CONFIG_PATH), type=argparse.FileType())
    args = parser.parse_args()

    config = load_config(args.config)

    for target in config.targets:
        pbs = PbsServer(**target.__dict__)
        collector = PbsCollector(pbs)
        collector.register()

    start_http_server(config)
    while True:
        sleep(1)
