import logging
from contextlib import asynccontextmanager

import config
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.search import router as search_router
from app.pipeline import router as pipeline_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: warm up graph. Shutdown: cleanup if needed."""
    from app.graph import get_sdr_graph
    get_sdr_graph()
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Log full traceback, return generic error to client."""
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in config.settings.cors_origins.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search_router)
app.include_router(pipeline_router)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import asyncio
    from app.graph import get_sdr_graph

    async def _run():
        graph = get_sdr_graph()
        result = await graph.ainvoke({"company_domain": "mediaexpert.pl"})
        print("Final state:", result)
        print("Qualified?", result.get("is_qualified"))
        print("Reason:", result.get("reason"))

    asyncio.run(_run())