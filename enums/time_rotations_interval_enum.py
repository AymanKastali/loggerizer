from enum import StrEnum


class TimeRotationIntervalEnum(StrEnum):
    SECONDS = "S"
    MINUTES = "M"
    HOURS = "H"
    DAYS = "D"
    MIDNIGHT = "midnight"
    MONDAY = "W0"
    TUESDAY = "W1"
    WEDNESDAY = "W2"
    THURSDAY = "W3"
    FRIDAY = "W4"
    SATURDAY = "W5"
    SUNDAY = "W6"

    @classmethod
    def values(cls) -> list[str]:
        """Return all allowed file intervals."""
        return [interval.value for interval in cls]
