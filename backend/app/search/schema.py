from pydantic import BaseModel, field_validator

from app.validators import validate_company_domain


class SearchRequest(BaseModel):
    company_domain: str

    @field_validator("company_domain")
    @classmethod
    def validate_domain(cls, v: str) -> str:
        return validate_company_domain(v)


class SearchResponse(BaseModel):
    website_content: str