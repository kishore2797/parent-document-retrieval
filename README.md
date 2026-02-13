## Project 10: Parent Document Retrieval

Full-stack app demonstrating **parent–child RAG**:

- **Small chunks** (children) used for vector retrieval.
- **Larger parent sections** used for the final LLM context window.
- Children are **linked to parents via metadata**, so we can expand precise hits into coherent context blocks.

### Structure

```text
parent-document-retrieval/
  backend/   # FastAPI: ingestion, parent+child chunking, parent-aware retrieval, RAG
  frontend/  # React + Vite: ingest docs, run queries, inspect children vs parents
```

### Quick start

**Backend**

```bash
cd parent-document-retrieval/backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # optional - set OPENAI_API_KEY for real answers
uvicorn app.main:app --reload --port 8003
```

**Frontend**

```bash
cd parent-document-retrieval/frontend
npm install
npm run dev
```

Dev UI defaults to `http://localhost:5177` and proxies `/api` to the backend.

