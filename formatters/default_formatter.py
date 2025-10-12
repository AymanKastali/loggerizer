from logging import Formatter, LogRecord
from typing import Literal


class DefaultFormatter(Formatter):
    DEFAULT_FORMAT = (
        "%(asctime)s | %(name)s | %(levelname)s | "
        "%(filename)s:%(lineno)d | %(funcName)s() | %(message)s"
    )
    DEFAULT_DATEFMT = "%Y-%m-%d %H:%M:%S"

    FormatStyle = Literal["%", "{", "$"]

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style: FormatStyle = "%",
    ) -> None:
        super().__init__(
            fmt=fmt or self.DEFAULT_FORMAT, datefmt=datefmt or self.DEFAULT_DATEFMT, style=style
        )

    def format(self, record: LogRecord) -> str:
        # Start with the main log line
        message = super().format(record)

        # Only add exception info if present
        if record.exc_info:
            exc_text = self.formatException(record.exc_info)
            exc_lines = exc_text.splitlines()
            exc_indented = "\n".join(f"    {line}" for line in exc_lines)
            message = f"{message}\n{exc_indented}"

        return message
