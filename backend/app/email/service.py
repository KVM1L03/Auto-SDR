import json
import logging
from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.agent.schema import AgentState
from config import settings

logger = logging.getLogger(__name__)

_PROMPTS_PATH = Path(__file__).parent / "prompts.json"
_prompts_cache: dict | None = None
_llm: ChatOpenAI | None = None


def _load_email_prompts() -> tuple[str, str]:
    """Load system_prompt and human_prompt from prompts.json (cached)."""
    global _prompts_cache
    if _prompts_cache is None:
        with open(_PROMPTS_PATH, encoding="utf-8") as f:
            _prompts_cache = json.load(f)
    return (
        _prompts_cache.get("system_prompt", ""),
        _prompts_cache.get("human_prompt", ""),
    )


def _get_llm() -> ChatOpenAI:
    """Return cached LLM (singleton)."""
    global _llm
    if _llm is None:
        _llm = ChatOpenAI(
            api_key=settings.openai_api_key.get_secret_value(),
            model="gpt-4o-mini",
            temperature=0,
            seed=42,
        )
    return _llm


async def email_node(state: AgentState) -> dict:
    """Generate cold email based on company domain and website content."""
    domain = state.get("company_domain", "")
    content = state.get("website_content", "")

    if not content or not domain:
        return {"draft_email": ""}

    try:
        system_prompt, human_template = _load_email_prompts()
        human_prompt = human_template.format(domain=domain, content=content)

        llm = _get_llm()
        result = await llm.ainvoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt),
        ])

        draft_email = result.content if hasattr(result, "content") else str(result)
        logger.info("Generated draft email for %s", domain)
        return {"draft_email": draft_email.strip()}
    except Exception as e:
        logger.exception("Email node error: %s", e)
        return {"draft_email": f"Error generating email: {str(e)}"}
