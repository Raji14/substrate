"""Input validation logic for credentials and wizard parameters."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class ValidationResult:
    is_valid: bool
    error_message: Optional[str] = None
    warning_message: Optional[str] = None
    formatted_value: Optional[str] = None


class InputValidator:
    """Validates user inputs with rich error messages and formatting."""

    API_KEY_PATTERNS = [
        re.compile(r"^sb-[a-zA-Z0-9_\-]{16,}$"),        # Substrate API key
        re.compile(r"^sk-ant-[a-zA-Z0-9_\-]{20,}$"),    # Anthropic API key
        re.compile(r"^sk-[a-zA-Z0-9_\-]{20,}$"),        # OpenAI / Standard key
        re.compile(r"^[a-zA-Z0-9_\-]{12,}$"),          # Generic token
    ]

    @classmethod
    def validate_api_key(cls, key: str, allow_empty: bool = False) -> ValidationResult:
        """Validate API key token format."""
        cleaned = key.strip()

        if not cleaned:
            if allow_empty:
                return ValidationResult(is_valid=True, formatted_value="")
            return ValidationResult(
                is_valid=False,
                error_message="API key cannot be empty. Enter your key or use /skip for local offline mode.",
            )

        if len(cleaned) < 8:
            return ValidationResult(
                is_valid=False,
                error_message=f"Key too short ({len(cleaned)} chars). Expected at least 8 characters.",
            )

        # Check against standard formats
        for pattern in cls.API_KEY_PATTERNS:
            if pattern.match(cleaned):
                return ValidationResult(
                    is_valid=True,
                    formatted_value=cleaned,
                )

        # Non-fatal format warning but valid
        return ValidationResult(
            is_valid=True,
            warning_message="Key does not match standard prefixes (sb-, sk-, sk-ant-), but proceeding.",
            formatted_value=cleaned,
        )

    @classmethod
    def mask_api_key(cls, key: str) -> str:
        """Create a secure masked representation of the API key."""
        cleaned = key.strip()
        if not cleaned:
            return ""
        if len(cleaned) <= 8:
            return "*" * len(cleaned)
        prefix = cleaned[:4]
        suffix = cleaned[-4:]
        masked_middle = "*" * max(4, min(16, len(cleaned) - 8))
        return f"{prefix}{masked_middle}{suffix}"
