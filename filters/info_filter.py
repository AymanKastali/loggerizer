from logging import INFO, Filter, LogRecord


class InfoFilter(Filter):
    def filter(self, record: LogRecord) -> bool:
        return record.levelno == INFO
