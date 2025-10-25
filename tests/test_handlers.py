import io
from logging import NullHandler, StreamHandler
from logging.handlers import (
    RotatingFileHandler,
    SMTPHandler,
    TimedRotatingFileHandler,
)

import pytest

from loggerizer.config import SMTPConfig
from loggerizer.enums import FileExtensionEnum, FileModeEnum
from loggerizer.handlers import (
    file_handler,
    null_handler,
    rotating_file_handler,
    smtp_handler,
    stream_handler,
    timed_rotating_file_handler,
)


def test_file_handler_valid(tmp_path):
    file = tmp_path / f"test{FileExtensionEnum.LOG.value}"
    handler = file_handler(str(file), mode=FileModeEnum.APPEND)
    assert hasattr(handler, "emit")
    assert handler.mode == FileModeEnum.APPEND.value  # type: ignore


def test_file_handler_invalid_extension(tmp_path):
    file = tmp_path / "test.invalid"
    with pytest.raises(ValueError) as exc_info:
        file_handler(str(file))
    assert "Invalid file extension" in str(exc_info.value)


def test_null_handler():
    handler = null_handler()
    assert isinstance(handler, NullHandler)


def test_stream_handler():
    stream = io.StringIO()
    handler = stream_handler(stream)
    assert isinstance(handler, StreamHandler)


def test_rotating_file_handler(tmp_path):
    file = tmp_path / f"rot{FileExtensionEnum.LOG.value}"
    handler = rotating_file_handler(str(file))
    assert isinstance(handler, RotatingFileHandler)


def test_timed_rotating_file_handler(tmp_path):
    file = tmp_path / f"timed{FileExtensionEnum.LOG.value}"
    handler = timed_rotating_file_handler(str(file))
    assert isinstance(handler, TimedRotatingFileHandler)


def test_smtp_handler():
    conf = SMTPConfig(
        host=("localhost", 1025),
        from_address="from@example.com",
        to_address=["to@example.com"],
        subject="Test",
    )
    handler = smtp_handler(conf)
    assert isinstance(handler, SMTPHandler)
    assert handler.fromaddr == conf.from_address
    assert handler.toaddrs == conf.to_address
