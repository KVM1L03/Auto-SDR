from typing import TypedDict

class AgentState(TypedDict, total=False):
    company_domain: str
    website_content: str
    is_qualified: bool
    reason: str
    draft_email: str