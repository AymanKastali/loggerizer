"""Builder pattern for creating custom loggers."""

from dataclasses import dataclass, field
from logging import Filter, Formatter, Handler, Logger, getLogger
from typing import Self

from loggerizer.enums import LogLevel
from loggerizer.formatters import DefaultFormatter


@dataclass
class LoggerBuilder:
    """Fluent builder for constructing loggers with custom configuration."""

    _name: str = "logger"
    _level: LogLevel = LogLevel.INFO
    _formatter: Formatter = field(default_factory=DefaultFormatter)
    _handlers: list[Handler] = field(default_factory=list)
    _filters: list[Filter] = field(default_factory=list)
    _propagate: bool = False

    def name(self, name: str) -> Self:
        """Set the logger name."""
        self._name = name
        return self

    def level(self, level: LogLevel) -> Self:
        """Set the logging level."""
        self._level = level
        return self

    def formatter(self, formatter: Formatter) -> Self:
        """Set the formatter for all handlers."""
        self._formatter = formatter
        return self

    def handler(self, handler: Handler) -> Self:
        """Add a handler."""
        if handler not in self._handlers:
            self._handlers.append(handler)
        return self

    def filter(self, log_filter: Filter) -> Self:
        """Add a filter."""
        if log_filter not in self._filters:
            self._filters.append(log_filter)
        return self

    def propagate(self, value: bool = True) -> Self:
        """Set whether to propagate to parent loggers."""
        self._propagate = value
        return self

    def build(self) -> Logger:
        """Build and return the configured logger."""
        logger = getLogger(self._name)
        logger.setLevel(self._level.value)
        logger.propagate = self._propagate

        # Clear existing handlers
        for h in list(logger.handlers):
            logger.removeHandler(h)

        # Add new handlers with formatter
        for h in self._handlers:
            h.setFormatter(self._formatter)
            h.setLevel(self._level.value)
            logger.addHandler(h)

        # Add filters
        for f in self._filters:
            logger.addFilter(f)

        return logger
