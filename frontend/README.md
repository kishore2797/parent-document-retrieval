## Parent Document Retrieval — Frontend

React + Vite UI for the parent–child RAG backend.

### Run

```bash
cd frontend
npm install
npm run dev
```

The dev server runs on `http://localhost:5177` and proxies `/api` to the backend at `http://localhost:8003`.

To point directly to a different backend URL, set:

```env
VITE_API_BASE_URL=http://localhost:8003
```

and remove/ignore the proxy.

