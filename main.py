from config import SMTPConfig
from enums import LogField
from loggers import LoggerFactory


def main():
    # Console logger with default fields only
    console_logger = LoggerFactory.console_logger(name="console_main", flat=True)
    console_logger.info("Console logger ready!")

    # Console JSON logger with extra fields
    console_json_logger = LoggerFactory.json_console_logger(
        name="console_json_main",
        extra_fields=[LogField.MODULE, LogField.THREAD_NAME, LogField.PROCESS],
    )
    console_json_logger.info("Console JSON logger ready!")

    # File logger with extra fields
    file_log = LoggerFactory.file_logger(
        name="file_main",
        filename="app",
        extra_fields=[LogField.MODULE, LogField.LINE_NO, LogField.FUNC_NAME],
        flat=True,
    )
    file_log.warning("File logger writing to app.log")

    # JSON file logger with extra fields
    json_log = LoggerFactory.json_file_logger(
        name="json_file_main",
        filename="events",
        extra_fields=[LogField.MODULE, LogField.THREAD_NAME, LogField.PROCESS],
    )
    json_log.debug("JSON log entry")

    # Timed rotating logger with extra fields
    timed = LoggerFactory.timed_rotating_logger(
        name="timed_logger",
        filename="timed_logs",
        extra_fields=[LogField.MODULE, LogField.PROCESS_NAME],
    )
    timed.info("Timed rotating log active")

    # Size rotating logger with extra fields
    rotating = LoggerFactory.size_rotating_logger(
        name="rotating_logger",
        filename="rotating_logs",
        extra_fields=[LogField.MODULE, LogField.LINE_NO],
    )
    rotating.info("Size rotating log active")

    # Null logger (no fields needed, always discarded)
    null_log = LoggerFactory.null_logger(name="null_main")
    null_log.info("This message is discarded")

    # SMTP logger with extra fields
    smtp_conf = SMTPConfig(
        host=("localhost", 1025),
        from_address="test@example.com",
        to_address=["admin@example.com"],
        subject="Critical Alert",
    )
    smtp_log = LoggerFactory.email_logger(
        name="smtp_main",
        smtp_config=smtp_conf,
        extra_fields=[LogField.MODULE, LogField.LINE_NO, LogField.FUNC_NAME],
    )
    smtp_log.error("Critical email sent!")


if __name__ == "__main__":
    main()
