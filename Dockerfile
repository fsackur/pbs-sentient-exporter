ARG PY_VERSION=3.13

FROM python:${PY_VERSION}-slim-bookworm

# TODO: remove (just for convenience)
RUN apt-get update \
    && apt-get install -y \
        iputils-ping \
        iputils-tracepath \
        telnet \
        net-tools \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /usr/local/lib/python3.13/site-packages/
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r /usr/local/lib/python3.13/site-packages/requirements.txt

COPY ./pbs_sentient_exporter /usr/local/lib/python3.13/site-packages/pbs_sentient_exporter
COPY ./pbs-sentient-exporter.py /usr/bin/pbs-sentient-exporter

ENV PBS_SENTIENT_EXPORTER_CONFIG=/config.yml
COPY ./sample.config.yml ${PBS_SENTIENT_EXPORTER_CONFIG}

ENTRYPOINT ["pbs-sentient-exporter"]

ARG DEFAULT_PORT=10038
ENV PBS_SENTIENT_EXPORTER_PORT=${DEFAULT_PORT}
EXPOSE ${PBS_SENTIENT_EXPORTER_PORT}
