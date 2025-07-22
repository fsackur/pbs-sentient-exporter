
from prometheus_client.core import GaugeMetricFamily

from . import BackupMetrics


def to_prom_metrics(pbs_metrics: BackupMetrics):
    size = GaugeMetricFamily("backup_size", "sum of file sizes", labels=["datastore", "backup", "type"], unit="B")
    size.add_metric(labels=[pbs_metrics.store, pbs_metrics.id, pbs_metrics.type], value=pbs_metrics.size)
    yield size

    last = GaugeMetricFamily("backup_last_finish_time", "finish time of last backup", labels=["datastore", "backup", "type"], unit="s")
    last.add_metric(labels=[pbs_metrics.store, pbs_metrics.id, pbs_metrics.type], value=pbs_metrics.last_finish_time)
    yield last
