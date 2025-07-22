import re
from io import TextIOWrapper
from typing import Annotated, Any, Literal, Optional

import yaml
from pydantic import (AfterValidator, AliasChoices, BaseModel, BeforeValidator,
                      Field, ValidationError)

from .logging import DEFAULT_LOG_LEVEL, LogLevel
from .pbs import PbsServerConfig

DEFAULT_ADDRESS = "0.0.0.0"
DEFAULT_PORT = 8000


DefaultCollector = Literal["gc"] | Literal["platform"] | Literal["process"]


def _parse_listen_address(value: Any) -> str:
    if ":" in value:
        address, port = value.split(":")
    elif re.match(r"^\d+$", value):
        address = ""
        port = value
    else:
        address = value
        port = ""
    return f"{address or DEFAULT_ADDRESS}:{port or DEFAULT_PORT}"


def _coerce_list(v):
    if isinstance(v, list):
        return v
    if isinstance(v, str):
        return [el.strip() for el in v.split(",")]
    return [v]


class ExporterConfig(BaseModel):
    listen_address: Annotated[str, Field(default=f":{DEFAULT_PORT}"), AfterValidator(_parse_listen_address)]
    certfile: Optional[str] = None
    keyfile: Optional[str] = None
    client_cafile: Optional[str] = None
    client_capath: Optional[str] = None
    drop: Annotated[list[DefaultCollector], Field(default=[]), BeforeValidator(_coerce_list)]
    log_level: Annotated[LogLevel, Field(default=DEFAULT_LOG_LEVEL)]


class Config(ExporterConfig):
    targets: Annotated[list[PbsServerConfig], Field(validation_alias=AliasChoices("targets", "target")), BeforeValidator(_coerce_list)]


def load_config(file: str | TextIOWrapper):
    file = file if isinstance(file, TextIOWrapper) else open(file, "r")
    try:
        config_raw = yaml.safe_load(file)
    finally:
        file.close()

    try:
        config = Config(**config_raw)
    except ValidationError:
        exporter = ExporterConfig(**config_raw)
        target = PbsServerConfig(**config_raw)
        config = Config(**exporter.__dict__, targets=[target])

    return config
