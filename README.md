# Logarizer Logger Examples

This document demonstrates how to use individual loggers from **Logarizer** separately without wrapping them in a main function.

---

## Console Logger

```python
from loggers import LoggerFactory

console = LoggerFactory.console_logger(name="console_main")
console.info("Console logger ready!")
```

## Console JSON Logger

```python
from loggers import LoggerFactory

console_json = LoggerFactory.json_console_logger(name="console_json_main")
console_json.info("Console JSON logger ready!")
```

## File Logger

```python
from loggers import LoggerFactory

file_log = LoggerFactory.file_logger(name="file_main", filename="app")
file_log.warning("File logger writing to app.log")
```

## JSON File Logger

```python
from loggers import LoggerFactory

json_log = LoggerFactory.json_file_logger(name="json_file_main", filename="events")
json_log.debug("JSON log entry")
```

## Timed Rotating Logger

```python
from loggers import LoggerFactory

timed = LoggerFactory.timed_rotating_logger(name="timed_logger", filename="timed_logs")
timed.info("Timed rotating log active")
```

## Size Rotating Logger

```python
from loggers import LoggerFactory

rotating = LoggerFactory.size_rotating_logger(name="rotating_logger", filename="rotating_logs")
rotating.info("Size rotating log active")
```

## Null Logger

```python
from loggers import LoggerFactory

null_log = LoggerFactory.null_logger(name="null_main")
null_log.info("This message is discarded")
```

## SMTP Logger

```python
from config.smtp_config import SMTPConfig
from loggers import LoggerFactory

smtp_conf = SMTPConfig(
    host=("localhost", 1025),
    from_address="test@example.com",
    to_address=["admin@example.com"],
    subject="Critical Alert",
)

smtp_log = LoggerFactory.email_logger(name="smtp_main", smtp_config=smtp_conf)
smtp_log.error("Critical email sent!")
```

---

### Logger Features

* **Console Logger**: Outputs logs to the console.
* **JSON Console Logger**: Outputs logs in JSON format.
* **File Logger**: Writes logs to a standard log file.
* **JSON File Logger**: Writes logs in JSON format.
* **Timed Rotating Logger**: Rotates logs based on time intervals.
* **Size Rotating Logger**: Rotates logs based on file size.
* **Null Logger**: Discards log messages.
* **SMTP Logger**: Sends error messages via email.
