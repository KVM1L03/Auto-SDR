from fastapi import HTTPException


def handle_external_api_error(exc: Exception) -> HTTPException:
    """Map external API errors to appropriate HTTP status."""
    msg = str(exc).lower()
    if "429" in str(exc) or "rate limit" in msg:
        return HTTPException(status_code=429, detail="Too many requests, try again later")
    return HTTPException(status_code=503, detail="Service temporarily unavailable")