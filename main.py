from loggers import LoggerFactory


def main():
    # Console logger
    console = LoggerFactory.console_logger()
    console.info("Console logger ready!")

    # Console JSON logger
    console = LoggerFactory.json_console_logger()
    console.info("Console logger ready!")

    # File logger
    file_log = LoggerFactory.file_logger(filename="app")
    file_log.warning("File logger writing to app.log")

    # JSON file logger
    json_log = LoggerFactory.json_file_logger(filename="events")
    json_log.debug("JSON log entry")

    # Rotating loggers
    timed = LoggerFactory.timed_rotating_logger()
    timed.info("Timed rotating log active")

    rotating = LoggerFactory.size_rotating_logger()
    rotating.info("Size rotating log active")

    # Null logger
    null_log = LoggerFactory.null_logger()
    null_log.info("This message is discarded")


if __name__ == "__main__":
    main()
