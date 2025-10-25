from logging import Handler, NullHandler


def null_handler() -> Handler:
    return NullHandler()
