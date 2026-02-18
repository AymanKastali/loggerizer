"""Factory for creating pre-configured loggers."""

from logging import Logger
from typing import TextIO

from loggerizer import handlers
from loggerizer.builder import LoggerBuilder
from loggerizer.config import SMTPConfig
from loggerizer.enums import FileMode, LogField, LogLevel, RotateWhen
from loggerizer.formatters import ColorFormatter, DefaultFormatter, JsonFormatter


class LoggerFactory:
    """Factory for creating common logger configurations."""

    @staticmethod
    def _builder(
        name: str,
        level: LogLevel = LogLevel.DEBUG,
    ) -> LoggerBuilder:
        return LoggerBuilder().name(name).level(level)

    @classmethod
    def null(cls, name: str = "null") -> Logger:
        """Create a logger that discards all output."""
        return cls._builder(name).handler(handlers.null()).build()

    @classmethod
    def console(
        cls,
        name: str = "console",
        level: LogLevel = LogLevel.DEBUG,
        fields: list[LogField] | None = None,
        flat: bool = False,
        stream: TextIO | None = None,
        colorize: bool = False,
    ) -> Logger:
        """Create a console logger with human-readable output."""
        formatter: DefaultFormatter
        if colorize:
            formatter = ColorFormatter(fields=fields, flat=flat, stream=stream)
        else:
            formatter = DefaultFormatter(fields=fields, flat=flat)
        return (
            cls._builder(name, level)
            .formatter(formatter)
            .handler(handlers.stream(stream))
            .build()
        )

    @classmethod
    def console_json(
        cls,
        name: str = "console_json",
        level: LogLevel = LogLevel.DEBUG,
        fields: list[LogField] | None = None,
        stream: TextIO | None = None,
    ) -> Logger:
        """Create a console logger with JSON output."""
        return (
            cls._builder(name, level)
            .formatter(JsonFormatter(fields=fields))
            .handler(handlers.stream(stream))
            .build()
        )

    @classmethod
    def file(
        cls,
        filename: str,
        name: str = "file",
        level: LogLevel = LogLevel.DEBUG,
        fields: list[LogField] | None = None,
        flat: bool = False,
        mode: FileMode = FileMode.APPEND,
        encoding: str = "utf-8",
    ) -> Logger:
        """Create a file logger with human-readable output."""
        return (
            cls._builder(name, level)
            .formatter(DefaultFormatter(fields=fields, flat=flat))
            .handler(handlers.file(filename, mode=mode, encoding=encoding))
            .build()
        )

    @classmethod
    def file_json(
        cls,
        filename: str,
        name: str = "file_json",
        level: LogLevel = LogLevel.DEBUG,
        fields: list[LogField] | None = None,
        mode: FileMode = FileMode.APPEND,
        encoding: str = "utf-8",
    ) -> Logger:
        """Create a file logger with JSON output."""
        return (
            cls._builder(name, level)
            .formatter(JsonFormatter(fields=fields))
            .handler(handlers.file(filename, mode=mode, encoding=encoding))
            .build()
        )

    @classmethod
    def rotating(
        cls,
        filename: str,
        name: str = "rotating",
        level: LogLevel = LogLevel.DEBUG,
        fields: list[LogField] | None = None,
        flat: bool = False,
        max_bytes: int = 10_000_000,
        backup_count: int = 5,
        encoding: str = "utf-8",
    ) -> Logger:
        """Create a size-based rotating file logger."""
        return (
            cls._builder(name, level)
            .formatter(DefaultFormatter(fields=fields, flat=flat))
            .handler(handlers.rotating(filename, max_bytes, backup_count, encoding))
            .build()
        )

    @classmethod
    def timed_rotating(
        cls,
        filename: str,
        name: str = "timed_rotating",
        level: LogLevel = LogLevel.DEBUG,
        fields: list[LogField] | None = None,
        flat: bool = False,
        when: RotateWhen = RotateWhen.MIDNIGHT,
        interval: int = 1,
        backup_count: int = 7,
        encoding: str = "utf-8",
    ) -> Logger:
        """Create a time-based rotating file logger."""
        return (
            cls._builder(name, level)
            .formatter(DefaultFormatter(fields=fields, flat=flat))
            .handler(
                handlers.timed_rotating(
                    filename, when, interval, backup_count, encoding
                )
            )
            .build()
        )

    @classmethod
    def email(
        cls,
        config: SMTPConfig,
        name: str = "email",
        level: LogLevel = LogLevel.ERROR,
        fields: list[LogField] | None = None,
        flat: bool = False,
    ) -> Logger:
        """Create an email logger for alerts."""
        return (
            cls._builder(name, level)
            .formatter(DefaultFormatter(fields=fields, flat=flat))
            .handler(handlers.smtp(config))
            .build()
        )
