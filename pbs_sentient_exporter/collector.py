
from prometheus_client.registry import REGISTRY, Collector

from .pbs import PbsServer, get_backup_metrics
from .map import get_size_metric, get_last_finished_metric, to_prom_metrics


class PbsCollector(Collector):
    def __init__(self, pbs: PbsServer):
        self.pbs = pbs

    def register(self):
        REGISTRY.register(self)

    def describe(self):
        yield get_size_metric()
        yield get_last_finished_metric()

    def collect(self):
        backup_metrics = get_backup_metrics(self.pbs)
        for bm in backup_metrics:
            yield from to_prom_metrics(bm)
