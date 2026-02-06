"""Type-safe enumerations for logger configuration."""

from enum import IntEnum, StrEnum
from logging import CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING


class LogLevel(IntEnum):
    """Logging severity levels."""

    NOTSET = NOTSET
    DEBUG = DEBUG
    INFO = INFO
    WARNING = WARNING
    ERROR = ERROR
    CRITICAL = CRITICAL


class LogField(StrEnum):
    """Available fields in log records."""

    ASC_TIME = "asctime"
    CREATED = "created"
    LEVEL_NAME = "levelname"
    LEVEL_NO = "levelno"
    MESSAGE = "message"
    NAME = "name"
    FILE_NAME = "filename"
    FUNC_NAME = "funcName"
    LINE_NO = "lineno"
    MODULE = "module"
    MSECS = "msecs"
    PATH_NAME = "pathname"
    PROCESS = "process"
    PROCESS_NAME = "processName"
    RELATIVE_CREATED = "relativeCreated"
    STACK_INFO = "stack_info"
    THREAD = "thread"
    THREAD_NAME = "threadName"
    TASK_NAME = "taskName"
    EXCEPTION = "exception"


class FileExtension(StrEnum):
    """Allowed log file extensions."""

    LOG = ".log"
    TXT = ".txt"
    JSON = ".json"
    CSV = ".csv"


class FileMode(StrEnum):
    """File open modes."""

    APPEND = "a"
    WRITE = "w"
    EXCLUSIVE = "x"


class RotateWhen(StrEnum):
    """Time-based rotation intervals."""

    SECONDS = "S"
    MINUTES = "M"
    HOURS = "H"
    DAYS = "D"
    MIDNIGHT = "midnight"
    MONDAY = "W0"
    TUESDAY = "W1"
    WEDNESDAY = "W2"
    THURSDAY = "W3"
    FRIDAY = "W4"
    SATURDAY = "W5"
    SUNDAY = "W6"
