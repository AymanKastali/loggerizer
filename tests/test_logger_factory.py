from logging import Logger, NullHandler, StreamHandler
from logging.handlers import SMTPHandler

import pytest

from loggerizer.config import SMTPConfig
from loggerizer.loggers import LoggerFactory


def test_null_logger():
    logger = LoggerFactory.null_logger()
    assert isinstance(logger, Logger)
    assert any(isinstance(h, NullHandler) for h in logger.handlers)


def test_console_logger():
    logger = LoggerFactory.console_logger()
    assert isinstance(logger, Logger)
    assert any(isinstance(h, StreamHandler) for h in logger.handlers)


def test_file_logger(tmp_path):
    file = tmp_path / "app_logs.log"
    logger = LoggerFactory.file_logger(filename=str(file))
    assert isinstance(logger, Logger)
    assert any(
        str(file) in getattr(h, "baseFilename", "") for h in logger.handlers
    )


def test_email_logger_requires_config():
    with pytest.raises(ValueError):
        LoggerFactory.email_logger()


def test_email_logger_with_config():
    conf = SMTPConfig(
        host=("localhost", 1025),
        from_address="from@example.com",
        to_address=["to@example.com"],
        subject="Test",
    )
    logger = LoggerFactory.email_logger(smtp_config=conf)
    assert any(isinstance(h, SMTPHandler) for h in logger.handlers)
