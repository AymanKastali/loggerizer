from dataclasses import dataclass, field
from logging import Filter, Formatter, Handler, Logger, getLogger
from typing import Self

from loggerizer.enums import LogLevelEnum
from loggerizer.formatters import DefaultFormatter


@dataclass
class LoggerBuilder:
    name: str = "default_logger"
    level: LogLevelEnum = LogLevelEnum.INFO
    formatter: Formatter = field(default_factory=DefaultFormatter)
    handlers: list[Handler] = field(default_factory=list)
    filters: list[Filter] = field(default_factory=list)

    def set_name(self, name: str) -> Self:
        self.name = name
        return self

    def set_level(self, level: LogLevelEnum) -> Self:
        self.level = level
        return self

    def set_formatter(self, formatter: Formatter) -> Self:
        self.formatter = formatter
        return self

    def add_handler(self, handler: Handler) -> Self:
        if handler not in self.handlers:
            self.handlers.append(handler)
        return self

    def add_filter(self, filter_obj: Filter) -> Self:
        if filter_obj not in self.filters:
            self.filters.append(filter_obj)
        return self

    def build(self) -> Logger:
        logger = getLogger(self.name)
        logger.setLevel(self.level.value)

        for h in list(logger.handlers):
            logger.removeHandler(h)

        for h in self.handlers:
            h.setFormatter(self.formatter)
            h.setLevel(self.level.value)
            logger.addHandler(h)

        for f in self.filters:
            logger.addFilter(f)

        return logger
