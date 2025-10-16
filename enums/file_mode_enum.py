from enum import StrEnum


class FileModeEnum(StrEnum):
    APPEND = "a"
    WRITE = "w"
    EXCLUSIVE = "x"

    @classmethod
    def values(cls) -> list[str]:
        """Return all allowed file modes."""
        return [member.value for member in cls]
