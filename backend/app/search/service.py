import logging

from tavily import AsyncTavilyClient

from app.agent.schema import AgentState
from config import settings

logger = logging.getLogger(__name__)

_tavily_client: AsyncTavilyClient | None = None


def _get_tavily_client() -> AsyncTavilyClient:
    """Return cached TavilyClient (singleton)."""
    global _tavily_client
    if _tavily_client is None:
        _tavily_client = AsyncTavilyClient(api_key=settings.tavily_api_key.get_secret_value())
    return _tavily_client


async def search_node(state: AgentState) -> dict:
    domain = state.get("company_domain", "").strip()
    if not domain:
        return {"website_content": ""}

    url = f"https://{domain}" if not domain.startswith("http") else domain

    try:
        client = _get_tavily_client()
        response = await client.extract(urls=[url])
        
        if not response.get("results"):
            return {"website_content": "No results found"}
        
        raw_content = response["results"][0].get("raw_content", "")
        return {"website_content": raw_content[:1000]}
    except Exception as e:
        logger.exception("Tavily extract failed: %s", e)
        raise