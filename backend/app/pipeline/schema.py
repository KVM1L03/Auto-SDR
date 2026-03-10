from pydantic import BaseModel


class PipelineRequest(BaseModel):
    company_domain: str


class PipelineResponse(BaseModel):
    """Clean response for frontend - domain, qualification status, reason, optional email."""
    company_domain: str
    is_qualified: bool
    reason: str
    draft_email: str | None = None
