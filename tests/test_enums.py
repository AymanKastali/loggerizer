from loggerizer.enums import (
    FileExtensionEnum,
    FileModeEnum,
    LogLevelEnum,
    TimeRotationIntervalEnum,
)


def test_file_extension_enum():
    values = FileExtensionEnum.values()
    assert ".log" in values
    assert ".csv" in values


def test_file_mode_enum():
    values = FileModeEnum.values()
    assert "a" in values
    assert "w" in values


def test_log_level_enum():
    values = LogLevelEnum.values()
    assert LogLevelEnum.DEBUG.value in values
    assert LogLevelEnum.CRITICAL.value in values


def test_time_rotation_interval_enum():
    values = TimeRotationIntervalEnum.values()
    assert "midnight" in values
    assert "H" in values
