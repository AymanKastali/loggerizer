from enum import StrEnum


class FileExtensionEnum(StrEnum):
    LOG = ".log"
    TXT = ".txt"
    JSON = ".json"
    CSV = ".csv"

    @classmethod
    def values(cls) -> list[str]:
        return [member.value for member in cls]
