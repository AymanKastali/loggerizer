from logging import FileHandler, Handler
from pathlib import Path

from loggerizer.enums import FileExtensionEnum, FileModeEnum


def file_handler(
    filename: str,
    mode: FileModeEnum = FileModeEnum.APPEND,
    encoding: str | None = "utf-8",
    delay: bool = False,
    errors: str | None = None,
) -> Handler:
    path = Path(filename)

    # Validate file extension
    if path.suffix not in FileExtensionEnum.values():
        raise ValueError(
            f"Invalid file extension '{path.suffix}'. Allowed: {', '.join(FileExtensionEnum.values())}"
        )

    return FileHandler(
        filename=filename,
        mode=mode.value,
        encoding=encoding,
        delay=delay,
        errors=errors,
    )
