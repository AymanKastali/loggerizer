import json
import traceback
from logging import Formatter, LogRecord
from typing import Any


class JsonFormatter(Formatter):
    """
    JSON Formatter for Python logging.
    Uses only built-in LogRecord attributes.
    """

    def __init__(self, datefmt="%Y-%m-%d %H:%M:%S") -> None:
        super().__init__(datefmt=datefmt)
        self.datefmt = datefmt

    def _format_exc_human(self, exc_info: Any) -> dict[str, Any]:
        if not exc_info:
            return {}

        exc_type, exc_value, exc_tb = exc_info

        frames = traceback.extract_tb(exc_tb) if exc_tb else []

        formatted_frames = [f"{frame.filename}:{frame.lineno} in {frame.name}" for frame in frames]

        return {
            "type": exc_type.__name__ if exc_type else None,
            "message": str(exc_value) if exc_value else None,
            "traceback": formatted_frames,
        }

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

        if record.exc_info:
            log_record["exception"] = self._format_exc_human(record.exc_info)

        clean_record = {k: v for k, v in log_record.items() if v is not None}
        return json.dumps(clean_record, ensure_ascii=False, indent=2)
