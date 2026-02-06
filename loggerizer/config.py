"""Configuration classes for loggerizer."""

from dataclasses import dataclass


@dataclass
class SMTPConfig:
    """SMTP server configuration for email logging."""

    host: tuple[str, int]
    from_address: str
    to_address: list[str]
    subject: str
    credentials: tuple[str, str] | None = None
    secure: tuple[()] | tuple[str] | tuple[str, str] | None = None
    timeout: float = 5.0
