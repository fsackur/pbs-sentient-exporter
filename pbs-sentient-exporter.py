#! /usr/bin/env python3

import argparse
import os
from time import sleep

from pbs_sentient_exporter import (PbsCollector, PbsServer, load_config,
                                   start_http_server)
from pbs_sentient_exporter.logging import get_logger

DEFAULT_CONFIG_PATH = "/etc/pbs-sentient-exporter/config.yml"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export metrics for Proxmox Backup Server to Prometheus")
    parser.add_argument("-c", "--config", default=os.environ.get("PBS_SENTIENT_EXPORTER_CONFIG", DEFAULT_CONFIG_PATH), type=argparse.FileType())
    args = parser.parse_args()

    config = load_config(args.config)
    logger = get_logger("", config.log_level)

    if any(t for t in config.targets if t.ignore_cert):
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        msg = urllib3.exceptions.InsecureRequestWarning("Unverified HTTPS requests are enabled.")
        logger.warning(msg)

    targets = [PbsServer(**t.__dict__, log_level=config.log_level) for t in config.targets]
    collector = PbsCollector(targets)
    collector.register()

    logger.info(f"Starting server on {config.listen_address}")
    start_http_server(config)
    while True:
        sleep(1)
