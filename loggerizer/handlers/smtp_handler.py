from logging import Handler
from logging.handlers import SMTPHandler

from loggerizer.config import SMTPConfig


def smtp_handler(config: SMTPConfig) -> Handler:
    return SMTPHandler(
        mailhost=config.host,
        fromaddr=config.from_address,
        toaddrs=config.to_address,
        subject=config.subject,
        credentials=config.credentials,
        secure=config.secure,
    )
