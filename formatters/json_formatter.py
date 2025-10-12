import json
from logging import Formatter, LogRecord


class JsonFormatter(Formatter):
    """
    JSON Formatter for Python logging.
    Uses only built-in LogRecord attributes.
    """

    def __init__(self, datefmt="%Y-%m-%d %H:%M:%S") -> None:
        super().__init__(datefmt=datefmt)
        self.datefmt = datefmt

    def format(self, record: LogRecord) -> str:
        log_record = {
            "asctime": self.formatTime(record, self.datefmt),
            "created": record.created,
            "levelname": record.levelname,
            "levelno": record.levelno,
            "message": record.getMessage(),
            "filename": record.filename,
            "funcName": record.funcName,
            "lineno": record.lineno,
            "module": record.module,
            "msecs": record.msecs,
            "name": record.name,
            "pathname": record.pathname,
            "process": record.process,
            "processName": record.processName,
            "relativeCreated": record.relativeCreated,
            "stack_info": record.stack_info if record.stack_info else None,
            "thread": record.thread,
            "threadName": record.threadName,
            "taskName": getattr(record, "taskName", None),
        }

        clean_record = {k: v for k, v in log_record.items() if v is not None}
        return json.dumps(clean_record, ensure_ascii=False, indent=2)
