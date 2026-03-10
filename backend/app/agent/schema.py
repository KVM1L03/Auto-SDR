from typing import TypedDict
from pydantic import BaseModel

class Qualification(BaseModel):
    is_qualified: bool
    reason: str

class AgentState(TypedDict, total=False):
    company_domain: str
    website_content: str
    is_qualified: bool
    reason: str
    draft_email: str