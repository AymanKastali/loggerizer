import io
from logging import NullHandler, StreamHandler
from logging.handlers import RotatingFileHandler, SMTPHandler, TimedRotatingFileHandler

import pytest

from loggerizer import FileExtension, FileMode, SMTPConfig, handlers


def test_file_handler_valid(tmp_path):
    filepath = tmp_path / f"test{FileExtension.LOG}"
    handler = handlers.file(str(filepath), mode=FileMode.APPEND)
    assert hasattr(handler, "emit")
    assert handler.mode == FileMode.APPEND


def test_file_handler_invalid_extension(tmp_path):
    filepath = tmp_path / "test.invalid"
    with pytest.raises(ValueError) as exc_info:
        handlers.file(str(filepath))
    assert "Invalid extension" in str(exc_info.value)


def test_null_handler():
    handler = handlers.null()
    assert isinstance(handler, NullHandler)


def test_stream_handler():
    output = io.StringIO()
    handler = handlers.stream(output)
    assert isinstance(handler, StreamHandler)


def test_rotating_handler(tmp_path):
    filepath = tmp_path / f"rot{FileExtension.LOG}"
    handler = handlers.rotating(str(filepath))
    assert isinstance(handler, RotatingFileHandler)


def test_timed_rotating_handler(tmp_path):
    filepath = tmp_path / f"timed{FileExtension.LOG}"
    handler = handlers.timed_rotating(str(filepath))
    assert isinstance(handler, TimedRotatingFileHandler)


def test_smtp_handler():
    conf = SMTPConfig(
        host=("localhost", 1025),
        from_address="from@example.com",
        to_address=["to@example.com"],
        subject="Test",
    )
    handler = handlers.smtp(conf)
    assert isinstance(handler, SMTPHandler)
    assert handler.fromaddr == conf.from_address
    assert handler.toaddrs == conf.to_address
