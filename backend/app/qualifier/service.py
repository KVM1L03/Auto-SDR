import json
import logging
from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.constants import END

from app.agent.schema import AgentState, Qualification
from config import settings

logger = logging.getLogger(__name__)

_PROMPTS_PATH = Path(__file__).parent / "prompts.json"
_system_prompt_cache: str | None = None
_structured_llm = None


def _load_system_prompt() -> str:
    """Load qualifier system prompt from prompts.json (cached)."""
    global _system_prompt_cache
    if _system_prompt_cache is None:
        with open(_PROMPTS_PATH, encoding="utf-8") as f:
            data = json.load(f)
        _system_prompt_cache = data.get("qualifier_system", "")
    return _system_prompt_cache


def _get_structured_llm():
    """Return cached structured LLM (singleton)."""
    global _structured_llm
    if _structured_llm is None:
        _structured_llm = (
            ChatOpenAI(
                api_key=settings.openai_api_key.get_secret_value(),
                model="gpt-4o-mini",
                temperature=0,
                seed=42,
            )
            .with_structured_output(Qualification)
        )
    return _structured_llm

async def qualifier_node(state: AgentState) -> dict:
    content = state.get("website_content", "")
    
    if not content or len(content.strip()) < 50:
        return {"is_qualified": False, "reason": "Not enough content to evaluate."}
    
    try:
        system_prompt = _load_system_prompt()
        structured_llm = _get_structured_llm()
        result = await structured_llm.ainvoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"WEBSITE CONTENT:\n{content}"),
        ])
        
        logger.info("Qualified: %s, reason: %s", result.is_qualified, result.reason)
        return {
            "is_qualified": result.is_qualified,
            "reason": result.reason,
        }
    except Exception as e:
        logger.exception("Qualifier node error: %s", e)
        return {
            "is_qualified": False, 
            "reason": f"System Error: {str(e)}"
        }

def route_lead(state: AgentState) -> str:
    """Early stopping - reject non-qualified leads."""
    if state.get("is_qualified"):
        return "email_node"
    return END