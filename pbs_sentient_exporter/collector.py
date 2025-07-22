
from prometheus_client.registry import REGISTRY, Collector

from . import PbsServer, get_backup_metrics, to_prom_metrics


class PbsCollector(Collector):
    def __init__(self, pbs: PbsServer):
        self.pbs = pbs

    def register(self):
        REGISTRY.register(self)

    def collect(self):
        backup_metrics = get_backup_metrics(self.pbs)
        return (to_prom_metrics(bm) for bm in backup_metrics)
