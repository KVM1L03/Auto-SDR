from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.search import router as search_router

app = FastAPI()
app.include_router(search_router)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    from app.search.service import search_node
    from app.agent.schema import AgentState
    
    test_state: AgentState = {"company_domain": "example.com"}
    result = search_node(test_state)
    print("Wynik search_node:", result)