from logging import Logger, StreamHandler

from loggerizer.enums import LogLevelEnum
from loggerizer.loggers import LoggerBuilder


def test_logger_builder_basic():
    logger = (
        LoggerBuilder().set_name("test").set_level(LogLevelEnum.DEBUG).build()
    )
    assert isinstance(logger, Logger)
    assert logger.level == LogLevelEnum.DEBUG.value


def test_logger_builder_add_handler_and_filter():
    handler = StreamHandler()
    logger = LoggerBuilder().add_handler(handler).build()
    assert any(h is handler for h in logger.handlers)
