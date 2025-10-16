from enum import StrEnum


class FileExtensionEnum(StrEnum):
    LOG = ".log"
    TXT = ".txt"
    JSON = ".json"
    CSV = ".csv"

    @classmethod
    def values(cls) -> list[str]:
        """Return all allowed file extensions."""
        return [member.value for member in cls]
