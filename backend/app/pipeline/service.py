import logging

from app.errors import handle_external_api_error
from app.graph import get_sdr_graph
from app.pipeline.schema import PipelineResponse

logger = logging.getLogger(__name__)


async def run_pipeline(company_domain: str) -> PipelineResponse:
    """Run full SDR pipeline: search → qualify → (email if qualified)."""
    graph = get_sdr_graph()
    try:
        result = await graph.ainvoke({"company_domain": company_domain})
    except Exception as e:
        logger.exception("Pipeline error: %s", e)
        raise handle_external_api_error(e) from e
    return PipelineResponse(
        company_domain=company_domain,
        is_qualified=result.get("is_qualified", False),
        reason=result.get("reason", ""),
        draft_email=result.get("draft_email"),
    )
