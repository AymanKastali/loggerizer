from loggerizer.config import SMTPConfig


def test_smtp_config_defaults():
    conf = SMTPConfig(
        host=("localhost", 25),
        from_address="from@example.com",
        to_address=["to@example.com"],
        subject="Test",
    )
    assert conf.host == ("localhost", 25)
    assert conf.timeout == 5.0
    assert conf.credentials is None
    assert conf.secure is None


def test_smtp_config_custom_values():
    conf = SMTPConfig(
        host=("smtp.example.com", 587),
        from_address="from@example.com",
        to_address=["to1@example.com", "to2@example.com"],
        subject="Custom",
        credentials=("user", "pass"),
        secure=("TLS",),
        timeout=10.0,
    )
    assert conf.host == ("smtp.example.com", 587)
    assert conf.credentials == ("user", "pass")
    assert conf.secure == ("TLS",)
    assert conf.timeout == 10.0
