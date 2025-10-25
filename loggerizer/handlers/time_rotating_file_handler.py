from logging import Handler
from logging.handlers import TimedRotatingFileHandler

from loggerizer.enums import TimeRotationIntervalEnum


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
