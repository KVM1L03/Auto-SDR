# Auto-SDR

**AI-powered Sales Development Representative pipeline** — Extract website content, qualify leads with an LLM, and generate personalized cold emails in one flow.

---

## 🔴 Demo: https://auto-sdr-mu.vercel.app

---

## Overview

Auto-SDR automates the early stages of outbound sales: it visits a company's website, extracts key information, determines whether the lead is qualified for outreach, and—if so—drafts a tailored cold email. Built with a modern stack and designed for both API and UI usage.

### Pipeline Flow

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐     ┌──────────────┐
│   Domain    │────▶│  Extract Content │────▶│  Qualify Lead   │────▶│ Generate     │
│   Input     │     │  (Tavily)        │     │  (LLM)          │     │ Email (LLM)  │
└─────────────┘     └──────────────────┘     └────────┬────────┘     └──────────────┘
                                                       │
                                            ┌──────────┴──────────┐
                                            │  Qualified?          │
                                            │  Yes → Email node    │
                                            │  No  → End           │
                                            └─────────────────────┘
```

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Backend** | Python 3.12, FastAPI | Async REST API |
| | LangGraph | Pipeline orchestration (state graph) |
| | LangChain + OpenAI | LLM for qualification & email generation |
| | Tavily | Web content extraction |
| | Pydantic | Config & validation |
| | Uvicorn | ASGI server |
| **Frontend** | React 19, TypeScript | UI |
| | Vite 7 | Build tool & dev server |
| | Tailwind CSS 4 | Styling |
| | Axios | HTTP client |

---

## Prerequisites

- **Python 3.12+** (backend)
- **Node.js 18+** (frontend)
- [OpenAI API key](https://platform.openai.com/api-keys)
- [Tavily API key](https://tavily.com/)
- *(Optional)* [LangSmith](https://smith.langchain.com/) for tracing

---

## Quick Start

### 1. Backend

**Option A: Docker (recommended)**

```bash
cd backend
cp .env.example .env
# Edit .env with your OPENAI_API_KEY and TAVILY_API_KEY
docker compose up --build
```

**Option B: Local**

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Linux/macOS
# or: venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
uvicorn main:app --reload
```

Backend runs at **http://localhost:8000**

### 2. Frontend

```bash
cd frontend
npm install
```

Create `.env` in `frontend/`:

```env
VITE_BASE_URL=http://localhost:8000/api
```

```bash
npm run dev
```

Frontend runs at **http://localhost:5173**

### 3. Use the app

1. Open http://localhost:5173
2. Enter a company domain (e.g. `example.com`)
3. Click **Analyze Lead**
4. View qualification status, reason, and draft email (with copy button)

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `TAVILY_API_KEY` | Yes | Tavily API key |
| `LANGCHAIN_API_KEY` | No | LangSmith API key for tracing |
| `LANGCHAIN_TRACING_V2` | No | Set to `true` to enable tracing |
| `LANGCHAIN_PROJECT` | No | LangSmith project name (default: `auto-sdr`) |
| `CORS_ORIGINS` | No | Comma-separated origins (default: `http://localhost:5173`) |

### Frontend (`frontend/.env`)

| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_BASE_URL` | Yes | Backend API base URL (e.g. `http://localhost:8000/api`) |

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/pipeline/` | Full SDR pipeline (extract → qualify → email) |
| `POST` | `/api/search/` | Extract website content only |

### Run full pipeline

```bash
curl -X POST http://localhost:8000/api/pipeline/ \
  -H "Content-Type: application/json" \
  -d '{"company_domain": "example.com"}'
```

**Response:**

```json
{
  "company_domain": "example.com",
  "is_qualified": true,
  "reason": "B2B SaaS company with clear pain points.",
  "draft_email": "Hi, I noticed that..."
}
```

### Interactive docs

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Project Structure

```
Auto-SDR/
├── backend/                 # FastAPI + LangGraph
│   ├── main.py              # App entry, CORS, health check
│   ├── config.py            # Pydantic settings
│   ├── app/
│   │   ├── graph.py         # LangGraph orchestration
│   │   ├── pipeline/        # Full SDR pipeline endpoint
│   │   ├── search/          # Search/extract endpoint
│   │   ├── qualifier/       # LLM qualification node
│   │   ├── email/           # Email generation node
│   │   ├── agent/           # State schemas
│   │   ├── validators.py    # Domain validation
│   │   └── errors.py       # HTTP error mapping
│   ├── requirements.txt
│   ├── Dockerfile
│   └── compose.yaml
│
└── frontend/                # React + Vite
    ├── src/
    │   ├── api/             # API client & pipeline types
    │   ├── components/      # PipelineResult, skeleton
    │   ├── App.tsx
    │   └── main.tsx
    ├── package.json
    └── vite.config.ts
```

---

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Invalid request (e.g. empty or invalid domain) |
| 422 | Validation error (Pydantic) |
| 429 | Rate limit exceeded (Tavily/OpenAI) |
| 503 | External service unavailable |

---

## License

MIT
