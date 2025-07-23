
from typing import Sequence

from prometheus_client.registry import REGISTRY, Collector

from .metrics import get_last_finished_metric, get_size_metric, to_prom_metrics
from .pbs import PbsServer, get_backup_metrics


class PbsCollector(Collector):
    targets: list[PbsServer]

    def __init__(self, targets: Sequence[PbsServer] | PbsServer | None = None):
        self.targets = [] if targets is None else list(targets) if isinstance(targets, Sequence) else [targets]

    def add_target(self, pbs: PbsServer):
        self.targets.append(pbs)

    def register(self):
        REGISTRY.register(self)

    def describe(self):
        yield get_size_metric()
        yield get_last_finished_metric()

    def collect(self):
        for pbs in self.targets:
            backup_metrics = get_backup_metrics(pbs)
            for bm in backup_metrics:
                yield from to_prom_metrics(pbs.label, bm)
