from loggerizer import FileExtension, FileMode, LogLevel, RotateWhen


def test_file_extension():
    assert FileExtension.LOG == ".log"
    assert FileExtension.CSV == ".csv"


def test_file_mode():
    assert FileMode.APPEND == "a"
    assert FileMode.WRITE == "w"


def test_log_level():
    assert LogLevel.DEBUG == 10
    assert LogLevel.CRITICAL == 50


def test_rotate_when():
    assert RotateWhen.MIDNIGHT == "midnight"
    assert RotateWhen.HOURS == "H"
