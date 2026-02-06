from logging import Handler
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from loggerizer.enums import FileExtensionEnum, TimeRotationIntervalEnum


def timed_rotating_file_handler(
    filename: str,
    when: TimeRotationIntervalEnum = TimeRotationIntervalEnum.MIDNIGHT,  # Time interval: "S", "M", "H", "D", "midnight", "W0"-"W6"
    interval: int = 1,  # every 1 day
    backup_count: int = 7,  # keep last 7 log files
    encoding: str | None = "utf-8",
    delay: bool = False,
    utc: bool = False,
    errors: str | None = None,
) -> Handler:
    path = Path(filename)
    if path.suffix not in FileExtensionEnum.values():
        raise ValueError(
            f"Invalid file extension '{path.suffix}'. Allowed: {', '.join(FileExtensionEnum.values())}"
        )

    return TimedRotatingFileHandler(
        filename=filename,
        when=when.value,
        interval=interval,
        backupCount=backup_count,
        encoding=encoding,
        delay=delay,
        utc=utc,
        errors=errors,
    )
