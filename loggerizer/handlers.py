"""Handler factory functions for different logging destinations."""

from logging import FileHandler, NullHandler, StreamHandler
from logging.handlers import RotatingFileHandler, SMTPHandler, TimedRotatingFileHandler
from pathlib import Path
from typing import TextIO

from loggerizer.config import SMTPConfig
from loggerizer.enums import FileExtension, FileMode, RotateWhen


def _validate_extension(filename: str) -> None:
    """Validate that file has an allowed extension."""
    suffix = Path(filename).suffix
    allowed = [e.value for e in FileExtension]
    if suffix not in allowed:
        raise ValueError(f"Invalid extension '{suffix}'. Allowed: {', '.join(allowed)}")


def null() -> NullHandler:
    """Create a no-op handler that discards all logs."""
    return NullHandler()


def stream(output: TextIO | None = None) -> StreamHandler:
    """Create a stream handler for console output."""
    return StreamHandler(output)


def file(
    filename: str,
    mode: FileMode = FileMode.APPEND,
    encoding: str = "utf-8",
    delay: bool = False,
) -> FileHandler:
    """Create a file handler for logging to a file."""
    _validate_extension(filename)
    return FileHandler(
        filename=filename,
        mode=mode.value,
        encoding=encoding,
        delay=delay,
    )


def rotating(
    filename: str,
    max_bytes: int = 10_000_000,
    backup_count: int = 5,
    encoding: str = "utf-8",
) -> RotatingFileHandler:
    """Create a size-based rotating file handler."""
    _validate_extension(filename)
    return RotatingFileHandler(
        filename=filename,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding=encoding,
    )


def timed_rotating(
    filename: str,
    when: RotateWhen = RotateWhen.MIDNIGHT,
    interval: int = 1,
    backup_count: int = 7,
    encoding: str = "utf-8",
    delay: bool = False,
    utc: bool = False,
) -> TimedRotatingFileHandler:
    """Create a time-based rotating file handler."""
    _validate_extension(filename)
    return TimedRotatingFileHandler(
        filename=filename,
        when=when.value,
        interval=interval,
        backupCount=backup_count,
        encoding=encoding,
        delay=delay,
        utc=utc,
    )


def smtp(config: SMTPConfig) -> SMTPHandler:
    """Create an SMTP handler for email alerts."""
    return SMTPHandler(
        mailhost=config.host,
        fromaddr=config.from_address,
        toaddrs=config.to_address,
        subject=config.subject,
        credentials=config.credentials,
        secure=config.secure,
        timeout=config.timeout,
    )
