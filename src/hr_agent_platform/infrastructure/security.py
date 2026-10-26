"""Security guardrails: PII redaction and Indirect Prompt Injection defense (OWASP LLM01, LLM06 & ASVS)."""

import re
from typing import ClassVar

from hr_agent_platform.domain.models import PIIEntity


class SecurityGuardrails:
    """Enterprise security sanitizer for candidate documents."""

    # Patterns for Brazilian and international PII
    CPF_PATTERN: ClassVar[re.Pattern] = re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")
    EMAIL_PATTERN: ClassVar[re.Pattern] = re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    )
    PHONE_PATTERN: ClassVar[re.Pattern] = re.compile(
        r"\b(?:\+?55\s?)?(?:\(?\d{2}\)?\s?)?(?:9\d{4}[-\s]?\d{4}|\d{4}[-\s]?\d{4})\b"
    )
    SSN_PATTERN: ClassVar[re.Pattern] = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

    # Prompt injection signatures (adversarial resumes, white text instructions, jailbreak markers)
    INJECTION_PATTERNS: ClassVar[list[re.Pattern]] = [
        re.compile(r"ignore\s+(all\s+)?(previous|prior)\s+instructions", re.IGNORECASE),
        re.compile(r"system\s*prompt\s*override", re.IGNORECASE),
        re.compile(
            r"you\s+must\s+rate\s+this\s+candidate\s+(as\s+)?(100|perfect|highest)",
            re.IGNORECASE,
        ),
        re.compile(r"disregard\s+the\s+rubric", re.IGNORECASE),
        re.compile(r"admin\s+mode\s*:\s*true", re.IGNORECASE),
        re.compile(r"<\s*script\s*>", re.IGNORECASE),
        re.compile(r"\[SYSTEM_NOTE:", re.IGNORECASE),
    ]

    @classmethod
    def sanitize(cls, text: str) -> tuple[str, list[PIIEntity], bool, list[str]]:
        sanitized = text
        detected_pii: list[PIIEntity] = []
        flags: list[str] = []
        has_injection = False

        # Redact CPFs
        for match in cls.CPF_PATTERN.finditer(text):
            val = match.group(0)
            placeholder = "[REDACTED_CPF]"
            detected_pii.append(PIIEntity("CPF", val, placeholder))
            sanitized = sanitized.replace(val, placeholder)

        # Redact Emails
        for match in cls.EMAIL_PATTERN.finditer(text):
            val = match.group(0)
            placeholder = "[REDACTED_EMAIL]"
            detected_pii.append(PIIEntity("EMAIL", val, placeholder))
            sanitized = sanitized.replace(val, placeholder)

        # Redact Phones
        for match in cls.PHONE_PATTERN.finditer(text):
            val = match.group(0)
            if len(val.strip()) >= 8:
                placeholder = "[REDACTED_PHONE]"
                detected_pii.append(PIIEntity("PHONE", val, placeholder))
                sanitized = sanitized.replace(val, placeholder)

        # Inspect Indirect Prompt Injection
        for pattern in cls.INJECTION_PATTERNS:
            if pattern.search(text):
                has_injection = True
                flag_name = f"SUSPECTED_PROMPT_INJECTION: {pattern.pattern}"
                flags.append(flag_name)

        return sanitized, detected_pii, has_injection, flags
