from logging import Logger, StreamHandler

from loggerizer import LoggerBuilder, LogLevel, handlers


def test_builder_basic():
    logger = LoggerBuilder().name("test").level(LogLevel.DEBUG).build()
    assert isinstance(logger, Logger)
    assert logger.level == LogLevel.DEBUG


def test_builder_with_handler():
    handler = StreamHandler()
    logger = LoggerBuilder().handler(handler).build()
    assert any(h is handler for h in logger.handlers)


def test_builder_with_handlers_module():
    logger = (
        LoggerBuilder()
        .name("test")
        .level(LogLevel.INFO)
        .handler(handlers.stream())
        .build()
    )
    assert isinstance(logger, Logger)
    assert any(isinstance(h, StreamHandler) for h in logger.handlers)
