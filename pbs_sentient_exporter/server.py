
import prometheus_client

from pbs_sentient_exporter import Config


def start_http_server(config: Config):
    addr, port = config.listen_address.split(":", 1)
    port = int(port)
    prometheus_client.start_http_server(
        port,
        addr=addr,
        certfile=config.certfile,
        keyfile=config.keyfile,
        client_cafile=config.client_cafile,
        client_capath=config.client_capath,
    )
