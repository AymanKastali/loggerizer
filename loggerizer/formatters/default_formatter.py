from logging import LogRecord

from loggerizer.formatters.base_formatter import BaseFormatter


class DefaultFormatter(BaseFormatter):
    """
    Human-readable formatter.
    Formats log records into a pipe-separated string.
    """

    def __init__(self, *args, flat: bool = False, **kwargs):
        """
        :param flat: If True, only log values separated by | without field names.
        """
        super().__init__(*args, **kwargs)
        self.flat = flat

    def format(self, record: LogRecord) -> str:
        data = self.record_to_dict(record)
        if self.flat:
            # Only log values in order
            return " | ".join(str(v) for v in data.values())
        # Include field names
        return " | ".join(f"{k}={v}" for k, v in data.items())
