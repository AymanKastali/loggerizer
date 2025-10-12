import json
from logging import Formatter, LogRecord
import traceback


class JsonFormatter(Formatter):
    """
    JSON Formatter for Python logging.
    Converts a LogRecord to a fully structured JSON object including exceptions.
    """

    def __init__(self, datefmt="%Y-%m-%d %H:%M:%S") -> None:
        super().__init__(datefmt=datefmt)
        self.datefmt = datefmt

    def format_exception_json(self, exc_info) -> dict:
        exc_type = exc_info[0].__name__ if exc_info[0] else None
        exc_message = str(exc_info[1]) if exc_info[1] else None
        tb_list = traceback.extract_tb(exc_info[2]) if exc_info[2] else []

        stack = [
            {
                "filename": frame.filename,
                "lineno": frame.lineno,
                "funcName": frame.name,
                "code": frame.line,
            }
            for frame in tb_list
        ]

        return {
            "type": exc_type,
            "message": exc_message,
            "stack": stack,
        }

    def format(self, record: LogRecord) -> str:
        exc_data = self.format_exception_json(record.exc_info) if record.exc_info else None

        log_record = {
            "asctime": self.formatTime(record, self.datefmt),
            "created": record.created,
            "exception": exc_data,
            "filename": record.filename,
            "funcName": record.funcName,
            "levelname": record.levelname,
            "levelno": record.levelno,
            "lineno": record.lineno,
            "message": record.getMessage(),
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

        # Remove None values
        clean_record = {k: v for k, v in log_record.items() if v is not None}

        return json.dumps(clean_record, ensure_ascii=False, indent=2)
