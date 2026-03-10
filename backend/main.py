from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.search import router as search_router
from app.pipeline import router as pipeline_router

app = FastAPI()
app.include_router(search_router)
app.include_router(pipeline_router)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    from app.graph import build_sdr_graph

    graph = build_sdr_graph()
    result = graph.invoke({"company_domain": "mediaexpert.pl"})
    print("Final state:", result)
    print("Qualified?", result.get("is_qualified"))
    print("Reason:", result.get("reason"))