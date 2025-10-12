from config.smtp_config import SMTPConfig
from loggers import LoggerFactory


def main():
    # Console JSON logger
    console_json = LoggerFactory.json_console_logger(name="console_json_main")
    console_json.info("Console JSON logger ready!")

    # File logger
    file_log = LoggerFactory.file_logger(name="file_main", filename="app")
    file_log.warning("File logger writing to app.log")

    # JSON file logger
    json_log = LoggerFactory.json_file_logger(name="json_file_main", filename="events")
    json_log.debug("JSON log entry")

    # Rotating loggers
    timed = LoggerFactory.timed_rotating_logger(name="timed_logger", filename="timed_logs")
    timed.info("Timed rotating log active")

    rotating = LoggerFactory.size_rotating_logger(name="rotating_logger", filename="rotating_logs")
    rotating.info("Size rotating log active")

    # Null logger
    null_log = LoggerFactory.null_logger(name="null_main")
    null_log.info("This message is discarded")

    # SMTP logger (example)
    smtp_conf = SMTPConfig(
        host=("localhost", 1025),
        from_address="test@example.com",
        to_address=["admin@example.com"],
        subject="Critical Alert",
    )
    smtp_log = LoggerFactory.email_logger(name="smtp_main", smtp_config=smtp_conf)
    smtp_log.error("Critical email sent!")


if __name__ == "__main__":
    main()
