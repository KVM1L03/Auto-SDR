from pydantic import BaseModel

class SearchRequest(BaseModel):
    company_domain: str

class SearchResponse(BaseModel):
    website_content: str