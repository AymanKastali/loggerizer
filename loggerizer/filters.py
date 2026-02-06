"""Log filters for selective logging."""

from logging import Filter, LogRecord

from loggerizer.enums import LogLevel


class LevelFilter(Filter):
    """Filter that only allows records matching a specific level."""

    def __init__(self, level: LogLevel) -> None:
        super().__init__()
        self.level = level

    def filter(self, record: LogRecord) -> bool:
        return record.levelno == self.level


class InfoFilter(LevelFilter):
    """Filter that only allows INFO level records."""

    def __init__(self) -> None:
        super().__init__(LogLevel.INFO)
