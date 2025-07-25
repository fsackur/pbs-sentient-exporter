
from prometheus_client.core import GaugeMetricFamily

from .pbs import BackupGroup

_label_names = ["instance", "datastore", "backup"]


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


def to_prom_metrics(server_label: str, pbs_metrics: BackupGroup):
    label_values = [server_label, pbs_metrics.store, f"{pbs_metrics.store}/{pbs_metrics.type}/{pbs_metrics.id}"]

    size = get_size_metric()
    size.add_metric(labels=label_values, value=pbs_metrics.size)
    yield size

    last = get_last_finished_metric()
    last.add_metric(labels=label_values, value=pbs_metrics.age)
    yield last
