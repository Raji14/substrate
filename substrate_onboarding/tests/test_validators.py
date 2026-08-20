"""Unit tests for input validator and key masker."""

from substrate_onboarding.engine.validator import InputValidator


def test_api_key_validations():
    # Valid Substrate key
    res = InputValidator.validate_api_key("sb-live-1234567890abcdef")
    assert res.is_valid is True

    # Valid OpenAI key
    res_oa = InputValidator.validate_api_key("sk-1234567890abcdefghijklmnop")
    assert res_oa.is_valid is True

    # Valid Anthropic key
    res_ant = InputValidator.validate_api_key("sk-ant-1234567890abcdefghijklmnop")
    assert res_ant.is_valid is True

    # Empty key error
    res_empty = InputValidator.validate_api_key("", allow_empty=False)
    assert res_empty.is_valid is False
    assert "cannot be empty" in res_empty.error_message

    # Empty key allowed
    res_empty_ok = InputValidator.validate_api_key("", allow_empty=True)
    assert res_empty_ok.is_valid is True

    # Too short
    res_short = InputValidator.validate_api_key("short")
    assert res_short.is_valid is False
    assert "too short" in res_short.error_message.lower()


def test_api_key_masking():
    assert InputValidator.mask_api_key("") == ""
    assert InputValidator.mask_api_key("short") == "*****"
    masked = InputValidator.mask_api_key("sb-live-1234567890abcdef")
    assert masked.startswith("sb-l")
    assert masked.endswith("cdef")
    assert "*" in masked
