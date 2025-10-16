from enum import StrEnum


class LogField(StrEnum):
    ASC_TIME = "asctime"
    LEVEL_NAME = "levelname"
    NAME = "name"
    MESSAGE = "message"
    CREATED = "created"
    LEVEL_NO = "levelno"
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

    @classmethod
    def values(cls) -> list[str]:
        """Return all allowed field values."""
        return [member.value for member in cls]
