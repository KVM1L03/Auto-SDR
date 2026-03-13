import logging

from fastapi import APIRouter

from app.agent.schema import AgentState
from app.errors import handle_external_api_error
from app.search.schema import SearchRequest, SearchResponse
from app.search.service import search_node

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/search", tags=["search"])


@router.post("/", response_model=SearchResponse)
async def search_endpoint(request: SearchRequest):
    state: AgentState = {"company_domain": request.company_domain}
    try:
        result = await search_node(state)
    except Exception as e:
        logger.exception("Search error: %s", e)
        raise handle_external_api_error(e) from e
    return SearchResponse(**result)