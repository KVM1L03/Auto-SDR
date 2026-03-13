from app.graph import get_sdr_graph
from app.pipeline.schema import PipelineResponse


async def run_pipeline(company_domain: str) -> PipelineResponse:
    """Run full SDR pipeline: search → qualify → (email if qualified)."""
    graph = get_sdr_graph()
    result = await graph.ainvoke({"company_domain": company_domain})
    return PipelineResponse(
        company_domain=company_domain,
        is_qualified=result.get("is_qualified", False),
        reason=result.get("reason", ""),
        draft_email=result.get("draft_email"),
    )
