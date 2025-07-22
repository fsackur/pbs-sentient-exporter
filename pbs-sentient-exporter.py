#! /usr/bin/env python3

import argparse
import os
from time import sleep

import yaml
from prometheus_client import start_http_server

from pbs_sentient_exporter import PbsCollector, PbsServer

DEFAULT_CONFIG_PATH = "/etc/pbs-sentient-exporter/config.yml"
DEFAULT_PORT = 8000

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export metrics for Proxmox Backup Server to Prometheus")
    parser.add_argument("-c", "--config", default=os.environ.get("PBS_SENTIENT_EXPORTER_CONFIG", DEFAULT_CONFIG_PATH), type=argparse.FileType())
    parser.add_argument("-p", "--port", default=os.environ.get("PBS_SENTIENT_EXPORTER_PORT", DEFAULT_PORT), type=int)
    args = parser.parse_args()

    port = args.port
    config = yaml.safe_load(args.config)

    pbs = PbsServer(**config)

    collector = PbsCollector(pbs)
    collector.register()

    start_http_server(port)
    while True:
        sleep(1)
