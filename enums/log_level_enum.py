from enum import IntEnum
from logging import CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING


class LogLevelEnum(IntEnum):
    """Strict enumeration of logging levels."""

    NOTSET = NOTSET
    DEBUG = DEBUG
    INFO = INFO
    WARNING = WARNING
    ERROR = ERROR
    CRITICAL = CRITICAL

    @classmethod
    def values(cls) -> list[int]:
        """Return all allowed file levels."""
        return [member.value for member in cls]
