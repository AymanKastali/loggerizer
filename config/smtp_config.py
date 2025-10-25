from dataclasses import dataclass


@dataclass
class SMTPConfig:
    host: tuple[str, int]
    from_address: str
    to_address: list[str]
    subject: str
    credentials: tuple[str, str] | None = None
    secure: tuple | None = None
    timeout: float = 5.0
