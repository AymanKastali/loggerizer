"""Log formatters for structured output."""

import json
import os
import sys
import traceback
from logging import Formatter, LogRecord
from typing import Any, TextIO

from loggerizer.enums import LogField

BOLD = "\033[1m"
DIM = "\033[90m"
LEVEL_COLORS: dict[str, str] = {
    "DEBUG": "\033[36m",
    "INFO": "\033[32m",
    "WARNING": "\033[33m",
    "ERROR": "\033[31m",
    "CRITICAL": "\033[91m",
}
RESET = "\033[0m"


def _enable_windows_ansi() -> None:
    """Enable ANSI escape code support on Windows terminals."""
    if os.name != "nt":
        return
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
        # STD_OUTPUT_HANDLE = -11, STD_ERROR_HANDLE = -12
        for handle_id in (-11, -12):
            handle = kernel32.GetStdHandle(handle_id)
            mode = ctypes.c_ulong()
            kernel32.GetConsoleMode(handle, ctypes.byref(mode))
            # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)
    except (AttributeError, OSError, ValueError):
        pass


_enable_windows_ansi()


def _supports_color(stream: TextIO | None = None) -> bool:
    """Check whether the given stream supports ANSI color output."""
    target = stream or sys.stderr
    return hasattr(target, "isatty") and target.isatty()


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
                f"{frame.filename}:{frame.lineno} in {frame.name}" for frame in frames
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


class ColorFormatter(DefaultFormatter):
    """Human-readable formatter with per-segment ANSI coloring.

    Applies the following color scheme:
      - Level name:  bold + level color, padded to fixed width
      - Message:     default terminal color (colored for ERROR/CRITICAL)
      - Exception:   colored traceback for ERROR/CRITICAL
      - Other fields (timestamp, logger name, etc.): dim
      - Separator:   dim

    Only colorizes output when the target stream is a TTY.
    Falls back to plain text when output is redirected or piped.
    """

    _LEVEL_PAD = max(len(name) for name in LEVEL_COLORS)
    _MESSAGE_FIELDS: set[str] = {LogField.MESSAGE}
    _LEVEL_FIELDS: set[str] = {LogField.LEVEL_NAME}
    _EXCEPTION_FIELDS: set[str] = {LogField.EXCEPTION}
    _ERROR_LEVELS: set[str] = {"ERROR", "CRITICAL"}

    def __init__(
        self,
        *args,
        stream: TextIO | None = None,
        colors: dict[str, str] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._colorize = _supports_color(stream)
        self._colors = {**LEVEL_COLORS, **(colors or {})}

    def _format_colored_exception(self, exc_data: dict[str, Any], color: str) -> str:
        lines = [
            f"{BOLD}{color}{exc_data['type']}: {exc_data.get('message', '')}{RESET}"
        ]
        for frame in exc_data.get("traceback", []):
            lines.append(f"  {color}{frame}{RESET}")
        return "\n".join(lines)

    def _colorize_value(
        self,
        key: str,
        value: Any,
        color: str,
        level: str,
    ) -> str:
        if key in self._LEVEL_FIELDS:
            padded = str(value).ljust(self._LEVEL_PAD)
            return f"{BOLD}{color}{padded}{RESET}"
        if key in self._EXCEPTION_FIELDS:
            if isinstance(value, dict) and level in self._ERROR_LEVELS:
                return self._format_colored_exception(value, color)
            return str(value)
        if key in self._MESSAGE_FIELDS:
            if level in self._ERROR_LEVELS:
                return f"{color}{value}{RESET}"
            return str(value)
        return f"{DIM}{value}{RESET}"

    def format(self, record: LogRecord) -> str:
        if not self._colorize:
            return super().format(record)

        data = self.to_dict(record)
        color = self._colors.get(record.levelname, "")
        separator = f" {DIM}\u2502{RESET} "

        if self.flat:
            parts = [
                self._colorize_value(k, v, color, record.levelname)
                for k, v in data.items()
            ]
        else:
            parts = [
                f"{DIM}{k}={RESET}{self._colorize_value(k, v, color, record.levelname)}"
                for k, v in data.items()
            ]
        return separator.join(parts)


class JsonFormatter(BaseFormatter):
    """JSON formatter for structured logging."""

    def __init__(self, *args, indent: int | None = 2, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.indent = indent

    def format(self, record: LogRecord) -> str:
        return json.dumps(self.to_dict(record), ensure_ascii=False, indent=self.indent)
