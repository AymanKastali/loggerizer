from dataclasses import dataclass


@dataclass
class SMTPConfig:
    host: tuple[str, int]  # SMTP server and port
    from_address: str  # Sender email
    to_address: list[str]  # list of recipients
    subject: str  # Email subject
    credentials: tuple[str, str] | None = None  # Username/password tuple
    secure: tuple | None = None  # For TLS/SSL (empty tuple for default)
    timeout: float = 5.0  # Connection timeout in seconds
