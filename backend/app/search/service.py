import os
from app.agent.schema import AgentState
from tavily import TavilyClient

def search_node(state: AgentState) -> dict:
    domain = state.get("company_domain", "").strip()
    if not domain:
        return {"website_content": ""}
    
    url = f"https://{domain}" if not domain.startswith("http") else domain
    
    try:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        response = client.extract(urls=[url])
        
        if not response.get("results"):
            return {"website_content": "No results found"}
        
        raw_content = response["results"][0].get("raw_content", "")
        return {"website_content": raw_content[:1000]}
    except Exception as e:
        return {"website_content": f"Error: {str(e)}"}