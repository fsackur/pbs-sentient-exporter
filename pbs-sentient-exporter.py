#! /usr/bin/env python3

import argparse
import os
from datetime import UTC, datetime

import yaml

from pbs_sentient_exporter import PbsServer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export metrics for Proxmox Backup Server to Prometheus")
    parser.add_argument("-c", "--config", default=os.environ.get("PBS_SENTIENT_EXPORTER_CONFIG", "./config.yml"))
    args = parser.parse_args()

    with open(args.config, "r") as file:
        config = yaml.safe_load(file)

    pbs = PbsServer(**config)

    response = pbs.get("admin/datastore")
    stores = response.json().get("data")
    store_names = [s["store"] for s in stores]

    for store_name in store_names:
        response = pbs.get(f"admin/datastore/{store_name}/groups")
        groups = response.json().get("data")
        for group in groups:
            last_backup = datetime.fromtimestamp(group.get("last-backup"), UTC)
            # print(store_name, group.get("backup-id"), last_backup, group.get("files"))

            response = pbs.get(f"admin/datastore/{store_name}/files", params={
                "backup-id": group.get("backup-id"),
                "backup-time": group.get("last-backup"),
                "backup-type": group.get("backup-type"),
            })

            files = response.json().get("data")
            # print(files)
            # size = sum([f.get("size", 0) for f in files])
            size = sum([f["size"] for f in files if f["filename"] != "client.log.blob"])
            # print(size)

            print(store_name, group.get("backup-id"), last_backup, size)
