import json
from logging import LogRecord

from loggerizer.formatters.base_formatter import BaseFormatter


class JsonFormatter(BaseFormatter):
    """
    JSON formatter.
    Converts log records to a structured JSON string.
    """

    def format(self, record: LogRecord) -> str:
        data = self.record_to_dict(record)
        return json.dumps(data, ensure_ascii=False, indent=2)
