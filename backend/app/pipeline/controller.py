from fastapi import APIRouter, HTTPException

from app.pipeline.schema import PipelineRequest, PipelineResponse
from app.pipeline.service import run_pipeline

router = APIRouter(prefix="/api/pipeline", tags=["pipeline"])


@router.post("/", response_model=PipelineResponse)
def pipeline_endpoint(request: PipelineRequest):
    """Run full SDR pipeline: search → qualify → (email if qualified)."""
    try:
        return run_pipeline(request.company_domain)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
