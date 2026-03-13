from fastapi import APIRouter
from app.search.service import search_node
from app.search.schema import SearchRequest, SearchResponse
from app.agent.schema import AgentState

router = APIRouter(prefix="/api/search", tags=["search"])

@router.post("/", response_model=SearchResponse)
async def search_endpoint(request: SearchRequest):
    state: AgentState = {"company_domain": request.company_domain}
    result = await search_node(state)
    return SearchResponse(**result)