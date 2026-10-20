from app.core.logging import REDACTED, redact_processor


def test_redacts_sensitive_keys() -> None:
    event = {
        "event": "x",
        "Authorization": "Bearer abc.def",
        "cookie": "pace_session=xyz",
        "api_key": "whatever",
        "headers": {"set-cookie": "a=b", "accept": "json"},
    }
    out = redact_processor(None, "info", event)
    assert out["Authorization"] == REDACTED
    assert out["cookie"] == REDACTED
    assert out["api_key"] == REDACTED
    assert out["headers"] == {"set-cookie": REDACTED, "accept": "json"}


def test_redacts_credential_looking_values_under_innocent_keys() -> None:
    event = {
        "event": "x",
        "detail": "calling with sk-ant-api03-FAKEFAKEFAKE",
        "url": "postgresql://pace:fake-pass@db.invalid/pace",
        "items": ["Bearer tok.en.value", "plain"],
    }
    out = redact_processor(None, "info", event)
    assert "sk-ant-" not in out["detail"]
    assert "fake-pass" not in out["url"]
    assert out["items"][0] == REDACTED
    assert out["items"][1] == "plain"
