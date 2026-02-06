import json
from logging import LogRecord

from loggerizer import BaseFormatter, DefaultFormatter, JsonFormatter, LogField, LogLevel


def create_sample_record() -> LogRecord:
    """Helper to create a sample LogRecord for testing."""
    return LogRecord(
        name="test",
        level=LogLevel.DEBUG,
        pathname="",
        lineno=1,
        msg="msg",
        args=(),
        exc_info=None,
    )


def test_base_formatter_to_dict():
    record = create_sample_record()
    fmt = BaseFormatter()
    d = fmt.to_dict(record)

    assert d[LogField.LEVEL_NAME] == "DEBUG"
    assert d[LogField.MESSAGE] == "msg"


def test_default_formatter_flat():
    record = create_sample_record()
    fmt = DefaultFormatter(flat=True)
    output = fmt.format(record)

    assert "|" in output


def test_default_formatter_named():
    record = create_sample_record()
    fmt = DefaultFormatter(flat=False)
    output = fmt.format(record)

    assert "levelname=DEBUG" in output
    assert "message=msg" in output


def test_json_formatter_output():
    record = create_sample_record()
    fmt = JsonFormatter()
    output = fmt.format(record)
    data = json.loads(output)

    assert data[LogField.LEVEL_NAME] == "DEBUG"
    assert data[LogField.MESSAGE] == "msg"
