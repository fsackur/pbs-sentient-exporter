
from prometheus_client.core import GaugeMetricFamily

from .pbs import BackupGroup

_label_names = ["datastore", "backup", "type"]


def get_size_metric():
    return GaugeMetricFamily(
        "backup_size",
        "sum of file sizes in bytes",
        labels=_label_names,
    )


def get_last_finished_metric():
    return GaugeMetricFamily(
        "backup_age",
        "time since last backup finished in seconds",
        labels=_label_names,
    )


def to_prom_metrics(pbs_metrics: BackupGroup):
    label_values = [pbs_metrics.store, pbs_metrics.id, pbs_metrics.type]

    size = get_size_metric()
    size.add_metric(labels=label_values, value=pbs_metrics.size)
    yield size

    last = get_last_finished_metric()
    last.add_metric(labels=label_values, value=pbs_metrics.age)
    yield last
