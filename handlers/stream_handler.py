from logging import Handler, StreamHandler
from typing import TextIO


def stream_handler(stream: TextIO | None = None) -> Handler:
    return StreamHandler(stream)
