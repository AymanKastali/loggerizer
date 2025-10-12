from logging import Handler
from logging.handlers import RotatingFileHandler


def rotating_file_handler(
    filename: str,
    max_bytes: int = 10_000_000,  # 9.5 MB
    backup_count: int = 5,
    encoding: str | None = "utf-8",
) -> Handler:
    return RotatingFileHandler(
        filename=filename, maxBytes=max_bytes, backupCount=backup_count, encoding=encoding
    )
