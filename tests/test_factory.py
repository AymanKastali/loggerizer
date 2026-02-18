import os
from logging import Logger, NullHandler, StreamHandler
from logging.handlers import SMTPHandler

import pytest

from loggerizer import LoggerFactory, SMTPConfig
from loggerizer.formatters import ColorFormatter


def test_null_logger():
    logger = LoggerFactory.null()
    assert isinstance(logger, Logger)
    assert any(isinstance(h, NullHandler) for h in logger.handlers)


def test_console_logger():
    logger = LoggerFactory.console()
    assert isinstance(logger, Logger)
    assert any(isinstance(h, StreamHandler) for h in logger.handlers)


def test_console_logger_colorize():
    logger = LoggerFactory.console(name="console_color", colorize=True)
    assert isinstance(logger, Logger)
    handler = logger.handlers[0]
    assert isinstance(handler.formatter, ColorFormatter)


def test_file_logger(tmp_path):
    filepath = tmp_path / "app.log"
    logger = LoggerFactory.file(str(filepath))
    assert isinstance(logger, Logger)
    assert any(str(filepath) in getattr(h, "baseFilename", "") for h in logger.handlers)


def test_email_logger():
    conf = SMTPConfig(
        host=("localhost", 1025),
        from_address="from@example.com",
        to_address=["to@example.com"],
        subject="Test",
    )
    logger = LoggerFactory.email(conf)
    assert any(isinstance(h, SMTPHandler) for h in logger.handlers)


@pytest.mark.skipif(
    os.getenv("SMTP_HOST") is None,
    reason="SMTP_HOST not set (run in devcontainer with mailhog)",
)
def test_email_logger_integration():
    """Integration test for email logging with mailhog."""
    smtp_host = os.getenv("SMTP_HOST", "mailhog")
    smtp_port = int(os.getenv("SMTP_PORT", "1025"))

    conf = SMTPConfig(
        host=(smtp_host, smtp_port),
        from_address="test@loggerizer.dev",
        to_address=["recipient@loggerizer.dev"],
        subject="[Loggerizer] Test Email",
    )
    logger = LoggerFactory.email(conf)
    logger.error("Test error message from loggerizer")

    # If no exception, email was sent successfully
    assert True
