# Loggerizer

A simple, powerful wrapper for Python's built-in logging module.

[![PyPI version](https://badge.fury.io/py/loggerizer.svg)](https://badge.fury.io/py/loggerizer)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

```bash
pip install loggerizer
```

## Quick Start

```python
from loggerizer import LoggerFactory

logger = LoggerFactory.console()
logger.info("Hello, World!")
```

## Logger Types

### Console Logger

```python
from loggerizer import LoggerFactory

logger = LoggerFactory.console()
logger.info("Human-readable console output")
```

### Console JSON Logger

```python
from loggerizer import LoggerFactory

logger = LoggerFactory.console_json()
logger.info("Structured JSON output")
```

### File Logger

```python
from loggerizer import LoggerFactory

logger = LoggerFactory.file("app.log")
logger.info("Logging to file")
```

### JSON File Logger

```python
from loggerizer import LoggerFactory

logger = LoggerFactory.file_json("app.json")
logger.info("JSON logging to file")
```

### Rotating Logger (by size)

```python
from loggerizer import LoggerFactory

logger = LoggerFactory.rotating(
    "app.log",
    max_bytes=10_000_000,  # 10MB
    backup_count=5
)
logger.info("Size-based rotation")
```

### Timed Rotating Logger

```python
from loggerizer import LoggerFactory, RotateWhen

logger = LoggerFactory.timed_rotating(
    "app.log",
    when=RotateWhen.MIDNIGHT,
    backup_count=7
)
logger.info("Time-based rotation")
```

### Email Logger

```python
from loggerizer import LoggerFactory, SMTPConfig

config = SMTPConfig(
    host=("smtp.example.com", 587),
    from_address="alerts@example.com",
    to_address=["admin@example.com"],
    subject="[ALERT] Application Error",
)

logger = LoggerFactory.email(config)
logger.error("Critical error occurred!")
```

### Null Logger

```python
from loggerizer import LoggerFactory

logger = LoggerFactory.null()
logger.info("This message is discarded")
```

## Custom Logger (Builder Pattern)

```python
from loggerizer import LoggerBuilder, handlers, LogLevel, LogField, DefaultFormatter

logger = (
    LoggerBuilder()
    .name("my_app")
    .level(LogLevel.DEBUG)
    .formatter(DefaultFormatter(
        fields=[LogField.ASC_TIME, LogField.LEVEL_NAME, LogField.MESSAGE, LogField.MODULE],
        flat=True
    ))
    .handler(handlers.stream())
    .handler(handlers.file("app.log"))
    .build()
)

logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```

## Adding Extra Data

```python
from loggerizer import LoggerFactory

logger = LoggerFactory.console_json()
logger.info("User action", extra={"user_id": 123, "action": "login", "ip": "192.168.1.1"})
```

## Custom Fields

```python
from loggerizer import LoggerFactory, LogField

logger = LoggerFactory.console(
    fields=[
        LogField.ASC_TIME,
        LogField.LEVEL_NAME,
        LogField.MESSAGE,
        LogField.MODULE,
        LogField.FUNC_NAME,
        LogField.LINE_NO,
    ]
)
logger.info("With extra context")
```

## Available Log Fields

| Field | Description |
|-------|-------------|
| `ASC_TIME` | Human-readable timestamp |
| `LEVEL_NAME` | Log level (DEBUG, INFO, etc.) |
| `MESSAGE` | Log message |
| `NAME` | Logger name |
| `MODULE` | Module name |
| `FUNC_NAME` | Function name |
| `LINE_NO` | Line number |
| `FILE_NAME` | File name |
| `PATH_NAME` | Full file path |
| `PROCESS` | Process ID |
| `THREAD` | Thread ID |
| `EXCEPTION` | Exception info |

## Handlers

```python
from loggerizer import handlers

handlers.stream()                    # Console output
handlers.file("app.log")             # File output
handlers.rotating("app.log")         # Size-based rotation
handlers.timed_rotating("app.log")   # Time-based rotation
handlers.smtp(config)                # Email alerts
handlers.null()                      # Discard logs
```

## License

MIT
