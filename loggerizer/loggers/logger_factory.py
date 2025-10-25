from logging import Logger
from typing import TextIO

from loggerizer.config import SMTPConfig
from loggerizer.enums import (
    FileModeEnum,
    LogField,
    LogLevelEnum,
    TimeRotationIntervalEnum,
)
from loggerizer.formatters import DefaultFormatter, JsonFormatter
from loggerizer.handlers import (
    file_handler,
    null_handler,
    rotating_file_handler,
    smtp_handler,
    stream_handler,
    timed_rotating_file_handler,
)
from loggerizer.loggers import LoggerBuilder


class LoggerFactory:
    """Factory for creating loggers with selectable fields and optional flat output."""

    @staticmethod
    def null_logger(name: str = "null_logger") -> Logger:
        return LoggerBuilder().set_name(name).add_handler(null_handler()).build()

    @staticmethod
    def json_file_logger(
        name: str = "json_logger",
        filename: str = "json_logs",
        mode: FileModeEnum = FileModeEnum.APPEND,
        encoding: str | None = "utf-8",
        delay: bool = False,
        errors: str | None = None,
        extra_fields: list[LogField] | None = None,
        flat: bool = False,  # added flat parameter for default formatter
    ) -> Logger:
        return (
            LoggerBuilder()
            .set_name(name)
            .set_level(LogLevelEnum.DEBUG)
            .set_formatter(JsonFormatter(extra_fields=extra_fields))
            .add_handler(
                file_handler(
                    f"{filename}.json",
                    mode=mode,
                    encoding=encoding,
                    delay=delay,
                    errors=errors,
                )
            )
            .build()
        )

    @staticmethod
    def file_logger(
        name: str = "file_logger",
        filename: str = "app_logs",
        mode: FileModeEnum = FileModeEnum.APPEND,
        encoding: str | None = "utf-8",
        delay: bool = False,
        errors: str | None = None,
        extra_fields: list[LogField] | None = None,
        flat: bool = False,
    ) -> Logger:
        return (
            LoggerBuilder()
            .set_name(name)
            .set_level(LogLevelEnum.DEBUG)
            .set_formatter(DefaultFormatter(extra_fields=extra_fields, flat=flat))
            .add_handler(
                file_handler(
                    filename=f"{filename}.log",
                    mode=mode,
                    encoding=encoding,
                    delay=delay,
                    errors=errors,
                )
            )
            .build()
        )

    @staticmethod
    def console_logger(
        name: str = "console_logger",
        stream: TextIO | None = None,
        extra_fields: list[LogField] | None = None,
        flat: bool = False,
    ) -> Logger:
        return (
            LoggerBuilder()
            .set_name(name)
            .set_level(LogLevelEnum.DEBUG)
            .set_formatter(DefaultFormatter(extra_fields=extra_fields, flat=flat))
            .add_handler(stream_handler(stream=stream))
            .build()
        )

    @staticmethod
    def json_console_logger(
        name: str = "console_json_logger",
        stream: TextIO | None = None,
        extra_fields: list[LogField] | None = None,
        flat: bool = False,  # flat is ignored for JSON, kept for API consistency
    ) -> Logger:
        return (
            LoggerBuilder()
            .set_name(name)
            .set_level(LogLevelEnum.DEBUG)
            .set_formatter(JsonFormatter(extra_fields=extra_fields))
            .add_handler(stream_handler(stream=stream))
            .build()
        )

    @staticmethod
    def timed_rotating_logger(
        name: str = "timed_rotating_logger",
        filename: str = "timed_logs",
        when: TimeRotationIntervalEnum = TimeRotationIntervalEnum.MIDNIGHT,
        interval: int = 1,
        backup_count: int = 7,
        encoding: str | None = "utf-8",
        delay: bool = False,
        utc: bool = False,
        errors: str | None = None,
        extra_fields: list[LogField] | None = None,
        flat: bool = False,
    ) -> Logger:
        return (
            LoggerBuilder()
            .set_name(name)
            .set_level(LogLevelEnum.DEBUG)
            .set_formatter(DefaultFormatter(extra_fields=extra_fields, flat=flat))
            .add_handler(
                timed_rotating_file_handler(
                    filename=f"{filename}.log",
                    when=when,
                    interval=interval,
                    backup_count=backup_count,
                    encoding=encoding,
                    delay=delay,
                    utc=utc,
                    errors=errors,
                )
            )
            .build()
        )

    @staticmethod
    def size_rotating_logger(
        name: str = "rotating_logger",
        filename: str = "rotating_logs",
        max_bytes: int = 10_000_000,
        backup_count: int = 5,
        encoding: str | None = "utf-8",
        extra_fields: list[LogField] | None = None,
        flat: bool = False,
    ) -> Logger:
        return (
            LoggerBuilder()
            .set_name(name)
            .set_level(LogLevelEnum.DEBUG)
            .set_formatter(DefaultFormatter(extra_fields=extra_fields, flat=flat))
            .add_handler(
                rotating_file_handler(
                    filename=f"{filename}.log",
                    max_bytes=max_bytes,
                    backup_count=backup_count,
                    encoding=encoding,
                )
            )
            .build()
        )

    @staticmethod
    def email_logger(
        name: str = "smtp_logger",
        smtp_config: SMTPConfig | None = None,
        extra_fields: list[LogField] | None = None,
        flat: bool = False,
    ) -> Logger:
        if smtp_config is None:
            raise ValueError("SMTP configuration is required for email logger")
        return (
            LoggerBuilder()
            .set_name(name)
            .set_level(LogLevelEnum.ERROR)
            .set_formatter(DefaultFormatter(extra_fields=extra_fields, flat=flat))
            .add_handler(smtp_handler(smtp_config))
            .build()
        )
