"""Log formatters for structured output."""

import json
import traceback
from logging import Formatter, LogRecord
from typing import Any

from loggerizer.enums import LogField


class BaseFormatter(Formatter):
    """
    Base formatter that converts LogRecord into a dictionary.
    Supports field selection and extra data extraction.
    """

    DEFAULT_FIELDS: list[LogField] = [
        LogField.ASC_TIME,
        LogField.LEVEL_NAME,
        LogField.NAME,
        LogField.MESSAGE,
    ]

    def __init__(
        self,
        *args,
        fields: list[LogField] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.fields = fields if fields is not None else self.DEFAULT_FIELDS.copy()

    def _format_exception(self, exc_info: Any) -> dict[str, Any] | None:
        if not exc_info:
            return None

        exc_type, exc_value, exc_tb = exc_info
        if exc_type is None:
            return None

        frames = traceback.extract_tb(exc_tb) if exc_tb else []
        return {
            "type": exc_type.__name__,
            "message": str(exc_value) if exc_value else None,
            "traceback": [
                f"{frame.filename}:{frame.lineno} in {frame.name}"
                for frame in frames
            ],
        }

    def _build_record(self, record: LogRecord) -> dict[str, Any]:
        return {
            LogField.ASC_TIME: self.formatTime(record, self.datefmt),
            LogField.CREATED: record.created,
            LogField.LEVEL_NAME: record.levelname,
            LogField.LEVEL_NO: record.levelno,
            LogField.MESSAGE: record.getMessage(),
            LogField.NAME: record.name,
            LogField.FILE_NAME: record.filename,
            LogField.FUNC_NAME: record.funcName,
            LogField.LINE_NO: record.lineno,
            LogField.MODULE: record.module,
            LogField.MSECS: record.msecs,
            LogField.PATH_NAME: record.pathname,
            LogField.PROCESS: record.process,
            LogField.PROCESS_NAME: record.processName,
            LogField.RELATIVE_CREATED: record.relativeCreated,
            LogField.STACK_INFO: record.stack_info,
            LogField.THREAD: record.thread,
            LogField.THREAD_NAME: record.threadName,
            LogField.TASK_NAME: getattr(record, "taskName", None),
            LogField.EXCEPTION: self._format_exception(record.exc_info),
        }

    def _get_extra(self, record: LogRecord) -> dict[str, Any]:
        reserved = {f.value for f in LogField} | {"msg", "args", "exc_info", "exc_text"}
        return {k: v for k, v in record.__dict__.items() if k not in reserved}

    def to_dict(self, record: LogRecord) -> dict[str, Any]:
        """Convert LogRecord to a dictionary with selected fields."""
        full = self._build_record(record)
        result = {f.value: full[f] for f in self.fields if full.get(f) is not None}

        extra = self._get_extra(record)
        if extra:
            result["extra"] = extra

        return result


class DefaultFormatter(BaseFormatter):
    """Human-readable pipe-separated formatter."""

    def __init__(self, *args, flat: bool = False, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.flat = flat

    def format(self, record: LogRecord) -> str:
        data = self.to_dict(record)
        if self.flat:
            return " | ".join(str(v) for v in data.values())
        return " | ".join(f"{k}={v}" for k, v in data.items())


class JsonFormatter(BaseFormatter):
    """JSON formatter for structured logging."""

    def __init__(self, *args, indent: int | None = 2, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.indent = indent

    def format(self, record: LogRecord) -> str:
        return json.dumps(self.to_dict(record), ensure_ascii=False, indent=self.indent)
