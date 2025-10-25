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

    def __init__(self, *args, extra_fields: Iterable[LogField] | None = None, **kwargs) -> None:
        """
        :param extra_fields: Optional iterable of LogField to include beyond defaults
        """
        super().__init__(*args, **kwargs)
        self.fields: list[LogField] = self.DEFAULT_FIELDS.copy()
        if extra_fields:
            for field in extra_fields:
                if field not in self.fields:
                    self.fields.append(field)

    def record_to_dict(self, record: LogRecord) -> dict[str, Any]:
        """Convert LogRecord to a dictionary of selected fields."""

        def format_exception(exc_info: Any) -> dict[str, Any]:
            if not exc_info:
                return {}

            match exc_info:
                case exc_type, exc_value, exc_tb:
                    frames = traceback.extract_tb(exc_tb) if exc_tb else []
                    return {
                        "type": exc_type.__name__ if exc_type else None,
                        "message": str(exc_value) if exc_value else None,
                        "traceback": [
                            f"{frame.filename}:{frame.lineno} in {frame.name}" for frame in frames
                        ],
                    }
            return {}

        # Full record dict
        full_record = {
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
                format_exception(record.exc_info) if record.exc_info else None
            ),
        }

        # Return only selected fields
        return {
            k: full_record[k]
            for k in (f.value for f in self.fields)
            if full_record.get(k) is not None
        }
