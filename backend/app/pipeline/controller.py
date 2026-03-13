from fastapi import APIRouter

from app.pipeline.schema import PipelineRequest, PipelineResponse
from app.pipeline.service import run_pipeline

router = APIRouter(prefix="/api/pipeline", tags=["pipeline"])


@router.post("/", response_model=PipelineResponse)
async def pipeline_endpoint(request: PipelineRequest):
    """Run full SDR pipeline: search → qualify → (email if qualified)."""
    return await run_pipeline(request.company_domain)
