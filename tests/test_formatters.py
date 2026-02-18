import io
import json
from logging import LogRecord

from loggerizer import (
    BaseFormatter,
    ColorFormatter,
    DefaultFormatter,
    JsonFormatter,
    LogField,
    LogLevel,
)
from loggerizer.formatters import BOLD, DIM, LEVEL_COLORS, RESET


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


class FakeTTY(io.StringIO):
    """A StringIO that reports itself as a TTY."""

    def isatty(self) -> bool:
        return True


def test_color_formatter_with_tty():
    record = create_sample_record()
    fmt = ColorFormatter(stream=FakeTTY())
    output = fmt.format(record)

    color = LEVEL_COLORS["DEBUG"]
    pad = ColorFormatter._LEVEL_PAD
    # Level name is bold + colored + padded + bracket-wrapped
    assert f"{BOLD}{color}{'DEBUG'.ljust(pad)}{RESET}" in output
    # Timestamp is dim
    assert f"{DIM}" in output
    # Message is plain (no color wrapping for DEBUG)
    assert "msg" in output


def test_color_formatter_without_tty():
    record = create_sample_record()
    fmt = ColorFormatter(stream=io.StringIO())
    output = fmt.format(record)

    assert "\033[" not in output


def test_color_formatter_preserves_record():
    record = create_sample_record()
    fmt = ColorFormatter(stream=FakeTTY())
    fmt.format(record)

    assert record.levelname == "DEBUG"


def test_color_formatter_all_levels():
    tty = FakeTTY()
    pad = ColorFormatter._LEVEL_PAD
    for level_name, color in LEVEL_COLORS.items():
        level_no = LogLevel[level_name].value
        record = LogRecord(
            name="test",
            level=level_no,
            pathname="",
            lineno=1,
            msg="msg",
            args=(),
            exc_info=None,
        )
        fmt = ColorFormatter(stream=tty)
        output = fmt.format(record)
        expected = f"{BOLD}{color}{level_name.ljust(pad)}{RESET}"
        assert expected in output


def test_color_formatter_dim_separator():
    record = create_sample_record()
    fmt = ColorFormatter(stream=FakeTTY())
    output = fmt.format(record)

    assert f"{DIM}\u2502{RESET}" in output


def test_color_formatter_flat_mode():
    record = create_sample_record()
    fmt = ColorFormatter(flat=True, stream=FakeTTY())
    output = fmt.format(record)

    pad = ColorFormatter._LEVEL_PAD
    color = LEVEL_COLORS["DEBUG"]
    assert f"{BOLD}{color}{'DEBUG'.ljust(pad)}{RESET}" in output
    assert "levelname=" not in output


def test_color_formatter_custom_colors():
    custom = {"DEBUG": "\033[35m"}  # magenta
    record = create_sample_record()
    fmt = ColorFormatter(stream=FakeTTY(), colors=custom)
    output = fmt.format(record)

    pad = ColorFormatter._LEVEL_PAD
    assert f"{BOLD}\033[35m{'DEBUG'.ljust(pad)}{RESET}" in output


def test_color_formatter_custom_colors_preserves_defaults():
    custom = {"DEBUG": "\033[35m"}
    tty = FakeTTY()
    record = LogRecord(
        name="test",
        level=LogLevel.WARNING,
        pathname="",
        lineno=1,
        msg="msg",
        args=(),
        exc_info=None,
    )
    fmt = ColorFormatter(stream=tty, colors=custom)
    output = fmt.format(record)

    pad = ColorFormatter._LEVEL_PAD
    warning_color = LEVEL_COLORS["WARNING"]
    expected = f"{BOLD}{warning_color}{'WARNING'.ljust(pad)}{RESET}"
    assert expected in output


def test_color_formatter_error_message_colored():
    tty = FakeTTY()
    record = LogRecord(
        name="test",
        level=LogLevel.ERROR,
        pathname="",
        lineno=1,
        msg="something broke",
        args=(),
        exc_info=None,
    )
    fmt = ColorFormatter(stream=tty)
    output = fmt.format(record)

    color = LEVEL_COLORS["ERROR"]
    assert f"{color}something broke{RESET}" in output


def test_color_formatter_critical_message_colored():
    tty = FakeTTY()
    record = LogRecord(
        name="test",
        level=LogLevel.CRITICAL,
        pathname="",
        lineno=1,
        msg="system down",
        args=(),
        exc_info=None,
    )
    fmt = ColorFormatter(stream=tty)
    output = fmt.format(record)

    color = LEVEL_COLORS["CRITICAL"]
    assert f"{color}system down{RESET}" in output


def test_color_formatter_info_message_not_colored():
    tty = FakeTTY()
    record = LogRecord(
        name="test",
        level=LogLevel.INFO,
        pathname="",
        lineno=1,
        msg="all good",
        args=(),
        exc_info=None,
    )
    fmt = ColorFormatter(stream=tty)
    output = fmt.format(record)

    # Message should appear without color wrapping
    assert "all good" in output
    # Ensure the message is NOT wrapped in the INFO color
    color = LEVEL_COLORS["INFO"]
    assert f"{color}all good{RESET}" not in output


def test_color_formatter_exception_colored():
    tty = FakeTTY()
    try:
        raise ValueError("test error")
    except ValueError:
        import sys as _sys

        exc_info = _sys.exc_info()

    record = LogRecord(
        name="test",
        level=LogLevel.ERROR,
        pathname="test_formatters.py",
        lineno=1,
        msg="something failed",
        args=(),
        exc_info=exc_info,
    )
    fmt = ColorFormatter(
        stream=tty,
        fields=[LogField.LEVEL_NAME, LogField.MESSAGE, LogField.EXCEPTION],
    )
    output = fmt.format(record)

    color = LEVEL_COLORS["ERROR"]
    # Exception type + message should be bold + colored
    assert f"{BOLD}{color}ValueError: test error{RESET}" in output
    # Traceback frames should be colored
    assert f"  {color}" in output
    assert "test_formatters.py:" in output


def test_color_formatter_exception_not_colored_for_info():
    tty = FakeTTY()
    try:
        raise RuntimeError("info exc")
    except RuntimeError:
        import sys as _sys

        exc_info = _sys.exc_info()

    record = LogRecord(
        name="test",
        level=LogLevel.INFO,
        pathname="test_formatters.py",
        lineno=1,
        msg="just info",
        args=(),
        exc_info=exc_info,
    )
    fmt = ColorFormatter(
        stream=tty,
        fields=[LogField.LEVEL_NAME, LogField.MESSAGE, LogField.EXCEPTION],
    )
    output = fmt.format(record)

    color = LEVEL_COLORS["INFO"]
    # Exception should NOT be colored for non-error levels
    assert f"{BOLD}{color}RuntimeError" not in output
