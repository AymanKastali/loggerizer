import traceback
from logging import Formatter, LogRecord
from typing import Any, Iterable

from loggerizer.enums import LogField


class BaseFormatter(Formatter):
    """
    Base formatter: converts LogRecord into a consistent dict.
    All other formatters derive from this.
    """

    # Default minimal fields
    DEFAULT_FIELDS: list[LogField] = [
        LogField.ASC_TIME,
        LogField.LEVEL_NAME,
        LogField.NAME,
        LogField.MESSAGE,
    ]

    def __init__(
        self, *args, extra_fields: Iterable[LogField] | None = None, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.fields: list[LogField] = self.DEFAULT_FIELDS.copy()
        if extra_fields:
            for field in extra_fields:
                if field not in self.fields:
                    self.fields.append(field)

    def _format_exception(self, exc_info: Any) -> dict[str, object]:
        if not exc_info:
            return {}

        match exc_info:
            case exc_type, exc_value, exc_tb:
                frames = traceback.extract_tb(exc_tb) if exc_tb else []
                return {
                    "type": exc_type.__name__ if exc_type else None,
                    "message": str(exc_value) if exc_value else None,
                    "traceback": [
                        f"{frame.filename}:{frame.lineno} in {frame.name}"
                        for frame in frames
                    ],
                }
        return {}

    def _build_standard_record(
        self, record: LogRecord
    ) -> dict[str, object | None]:
        return {
            LogField.ASC_TIME.value: self.formatTime(record, self.datefmt),
            LogField.CREATED.value: record.created,
            LogField.LEVEL_NAME.value: record.levelname,
            LogField.LEVEL_NO.value: record.levelno,
            LogField.MESSAGE.value: record.getMessage(),
            LogField.FILE_NAME.value: record.filename,
            LogField.FUNC_NAME.value: record.funcName,
            LogField.LINE_NO.value: record.lineno,
            LogField.MODULE.value: record.module,
            LogField.MSECS.value: record.msecs,
            LogField.NAME.value: record.name,
            LogField.PATH_NAME.value: record.pathname,
            LogField.PROCESS.value: record.process,
            LogField.PROCESS_NAME.value: record.processName,
            LogField.RELATIVE_CREATED.value: record.relativeCreated,
            LogField.STACK_INFO.value: record.stack_info or None,
            LogField.THREAD.value: record.thread,
            LogField.THREAD_NAME.value: record.threadName,
            LogField.TASK_NAME.value: getattr(record, "taskName", None),
            LogField.EXCEPTION.value: (
                self._format_exception(record.exc_info)
                if record.exc_info
                else None
            ),
        }

    def _build_extra(self, record: LogRecord) -> dict[str, object]:
        reserved_keys = set(LogField.values()) | {
            "msg",
            "args",
            "exc_info",
            "exc_text",
        }

        return {
            k: v for k, v in record.__dict__.items() if k not in reserved_keys
        }

    def _return_log_response(
        self, full_record, user_extra
    ) -> dict[str, object | dict[str, object]]:
        return {
            k: full_record[k]
            for k in (f.value for f in self.fields)
            if full_record.get(k) is not None
        } | ({"extra": user_extra} if user_extra else {})

    def record_to_dict(
        self, record: LogRecord
    ) -> dict[str, object | dict[str, object]]:
        """Convert LogRecord to a dictionary of selected fields."""

        full_record = self._build_standard_record(record)
        extra = self._build_extra(record)

        if extra:
            full_record["extra"] = extra

        return self._return_log_response(full_record, extra)
