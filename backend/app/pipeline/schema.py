from pydantic import BaseModel, field_validator

from app.validators import validate_company_domain


class PipelineRequest(BaseModel):
    company_domain: str

    @field_validator("company_domain")
    @classmethod
    def validate_domain(cls, v: str) -> str:
        return validate_company_domain(v)


class PipelineResponse(BaseModel):
    """Clean response for frontend - domain, qualification status, reason, optional email."""
    company_domain: str
    is_qualified: bool
    reason: str
    draft_email: str | None = None
