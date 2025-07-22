#! /usr/bin/env python3

import argparse
import os
from time import sleep

import yaml
from prometheus_client import start_http_server

from pbs_sentient_exporter import PbsCollector, PbsServer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export metrics for Proxmox Backup Server to Prometheus")
    parser.add_argument("-c", "--config", default=os.environ.get("PBS_SENTIENT_EXPORTER_CONFIG", "./config.yml"), type=argparse.FileType())
    parser.add_argument("-p", "--port", default=os.environ.get("PBS_SENTIENT_EXPORTER_PORT", 8000), type=int)
    args = parser.parse_args()

    port = args.port
    config = yaml.safe_load(args.config)

    pbs = PbsServer(**config)

    collector = PbsCollector(pbs)
    collector.register()

    start_http_server(port)
    while True:
        sleep(1)
