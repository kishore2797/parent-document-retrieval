## Parent Document Retrieval — Backend

FastAPI service that implements **parent–child RAG**:

- Ingest documents as larger parent sections.
- Split parents into small overlapping child chunks for vector retrieval.
- At query time, retrieve children and expand back to parents for the final context window.

### Endpoints

- `GET /health` — Liveness.
- `POST /documents` — Ingest documents.
  - Body: `{"documents": [{ "title": "...", "text": "...", "doc_id": "optional" }] }`
  - Response: `{ "parents_created": N, "children_created": M }`
- `POST /query` — Parent-aware RAG query.
  - Body:
    - `query`: user question
    - `top_children` (optional): override default number of child hits
    - `max_parents` (optional): override number of parents in context
    - `generate_answer` (default `true`)
  - Response:
    - `children`: retrieved child hits (small chunks)
    - `parents`: expanded parent contexts actually shown to the LLM
    - `answer`: optional final answer

### Running

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # and set OPENAI_API_KEY if you want real answers
uvicorn app.main:app --reload --port 8003
```

