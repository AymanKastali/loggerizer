"""
Loggerizer - A simple, powerful wrapper for Python's logging module.

Quick Start:
    from loggerizer import LoggerFactory

    logger = LoggerFactory.console()
    logger.info("Hello, World!")

Custom Logger:
    from loggerizer import LoggerBuilder, handlers, LogLevel

    logger = (
        LoggerBuilder()
        .name("my_app")
        .level(LogLevel.DEBUG)
        .handler(handlers.file("app.log"))
        .build()
    )
"""

from loggerizer import handlers
from loggerizer.builder import LoggerBuilder
from loggerizer.config import SMTPConfig
from loggerizer.enums import FileExtension, FileMode, LogField, LogLevel, RotateWhen
from loggerizer.factory import LoggerFactory
from loggerizer.filters import InfoFilter, LevelFilter
from loggerizer.formatters import BaseFormatter, DefaultFormatter, JsonFormatter

__all__ = [
    # Core
    "LoggerFactory",
    "LoggerBuilder",
    # Handlers module
    "handlers",
    # Formatters
    "BaseFormatter",
    "DefaultFormatter",
    "JsonFormatter",
    # Filters
    "LevelFilter",
    "InfoFilter",
    # Config
    "SMTPConfig",
    # Enums
    "LogLevel",
    "LogField",
    "FileExtension",
    "FileMode",
    "RotateWhen",
]
