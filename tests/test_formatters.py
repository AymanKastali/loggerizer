import json
from logging import LogRecord

from loggerizer.enums import LogField, LogLevelEnum
from loggerizer.formatters import BaseFormatter, DefaultFormatter, JsonFormatter


def create_sample_record() -> LogRecord:
    """Helper to create a sample LogRecord for testing."""
    return LogRecord(
        name="test",
        level=LogLevelEnum.DEBUG.value,  # Use enum
        pathname="",
        lineno=1,
        msg="msg",
        args=(),
        exc_info=None,
    )


def test_base_formatter_record_to_dict():
    record = create_sample_record()
    fmt = BaseFormatter()
    d = fmt.record_to_dict(record)

    assert d[LogField.LEVEL_NAME.value] == LogLevelEnum.DEBUG.name
    assert d[LogField.MESSAGE.value] == "msg"


def test_default_formatter_flat():
    record = create_sample_record()
    fmt = DefaultFormatter(flat=True)
    output = fmt.format(record)

    # Flat output should contain pipe separators
    assert "|" in output


def test_default_formatter_named():
    record = create_sample_record()
    fmt = DefaultFormatter(flat=False)
    output = fmt.format(record)

    # Named output should include field names
    assert f"{LogField.LEVEL_NAME.value}={LogLevelEnum.DEBUG.name}" in output
    assert f"{LogField.MESSAGE.value}=msg" in output


def test_json_formatter_output():
    record = create_sample_record()
    fmt = JsonFormatter()
    output = fmt.format(record)
    data = json.loads(output)

    assert data[LogField.LEVEL_NAME.value] == LogLevelEnum.DEBUG.name
    assert data[LogField.MESSAGE.value] == "msg"
