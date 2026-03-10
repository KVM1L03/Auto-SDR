from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.search import router as search_router
from app.search.schema import SearchRequest
from app.graph import build_sdr_graph

app = FastAPI()
app.include_router(search_router)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/pipeline")
def run_pipeline(request: SearchRequest):
    """Run full SDR pipeline: search → qualify → (email if qualified)."""
    graph = build_sdr_graph()
    result = graph.invoke({"company_domain": request.company_domain})
    return result

if __name__ == "__main__":
    from app.graph import build_sdr_graph

    graph = build_sdr_graph()
    result = graph.invoke({"company_domain": "mediaexpert.pl"})
    print("Final state:", result)
    print("Qualified?", result.get("is_qualified"))
    print("Reason:", result.get("reason"))