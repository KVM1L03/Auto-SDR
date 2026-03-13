import re


def validate_company_domain(v: str) -> str:
    """Validate and normalize company domain. Raises ValueError on invalid input."""
    v = (v or "").strip()
    if not v:
        raise ValueError("company_domain is required")
    pattern = r"^[a-zA-Z0-9][a-zA-Z0-9.-]*\.[a-zA-Z]{2,}$"
    if not re.match(pattern, v):
        raise ValueError("Invalid domain format")
    return v
