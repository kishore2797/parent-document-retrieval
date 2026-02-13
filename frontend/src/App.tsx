import { useCallback, useState } from "react";
import {
  api,
  type ChildHit,
  type IngestRequest,
  type IngestResponse,
  type ParentContext,
  type QueryRequest,
  type QueryResponse,
} from "./lib/api";

function ChildList({ childrenHits }: { childrenHits: ChildHit[] }) {
  if (!childrenHits.length) {
    return <p className="muted">No child hits yet.</p>;
  }
  return (
    <div>
      {childrenHits.map((c) => (
        <div key={c.id} className="parent-block">
          <div className="child-meta">
            score {c.score.toFixed(3)} · parent {c.parent_id} · doc {c.doc_id}
            {c.title ? ` · ${c.title}` : ""}
          </div>
          <div className="child-snippet">{c.snippet}</div>
        </div>
      ))}
    </div>
  );
}

function ParentList({ parents }: { parents: ParentContext[] }) {
  if (!parents.length) {
    return <p className="muted">No parent sections selected.</p>;
  }
  return (
    <div>
      {parents.map((p) => (
        <div key={p.parent_id} className="parent-block">
          <div className="parent-header">
            [{p.title || p.parent_id}] · doc {p.doc_id} · score {p.score.toFixed(3)}
          </div>
          <div>{p.text}</div>
        </div>
      ))}
    </div>
  );
}

export default function App() {
  const [title, setTitle] = useState("");
  const [text, setText] = useState("");
  const [ingestStatus, setIngestStatus] = useState<string | null>(null);
  const [ingestLoading, setIngestLoading] = useState(false);

  const [query, setQuery] = useState("");
  const [topChildren, setTopChildren] = useState<number>(30);
  const [maxParents, setMaxParents] = useState<number>(4);
  const [generateAnswer, setGenerateAnswer] = useState(true);
  const [result, setResult] = useState<QueryResponse | null>(null);
  const [queryError, setQueryError] = useState<string | null>(null);
  const [queryLoading, setQueryLoading] = useState(false);

  const handleIngest = useCallback(async () => {
    if (!title.trim() || !text.trim()) return;
    setIngestLoading(true);
    setIngestStatus(null);
    try {
      const body: IngestRequest = {
        documents: [{ title: title.trim(), text: text.trim() }],
      };
      const res = await api.post<IngestResponse>("/documents", body);
      setIngestStatus(
        `Created ${res.data.parents_created} parent(s) and ${res.data.children_created} child chunk(s).`,
      );
      setText("");
    } catch (err: unknown) {
      const msg =
        err && typeof err === "object" && "response" in err
          ? String(
              (err as { response?: { data?: { detail?: string } } }).response?.data?.detail ??
                "Ingest failed",
            )
          : "Ingest failed";
      setIngestStatus(msg);
    } finally {
      setIngestLoading(false);
    }
  }, [title, text]);

  const handleQuery = useCallback(async () => {
    if (!query.trim()) return;
    setQueryLoading(true);
    setQueryError(null);
    setResult(null);
    try {
      const body: QueryRequest = {
        query: query.trim(),
        top_children: topChildren,
        max_parents: maxParents,
        generate_answer: generateAnswer,
      };
      const res = await api.post<QueryResponse>("/query", body);
      setResult(res.data);
    } catch (err: unknown) {
      const msg =
        err && typeof err === "object" && "response" in err
          ? String(
              (err as { response?: { data?: { detail?: string } } }).response?.data?.detail ??
                "Query failed",
            )
          : "Query failed";
      setQueryError(msg);
    } finally {
      setQueryLoading(false);
    }
  }, [query, topChildren, maxParents, generateAnswer]);

  return (
    <div>
      <header style={{ marginBottom: "1.5rem" }}>
        <h1>Parent Document Retrieval</h1>
        <p className="muted">
          Retrieve with small chunks, but answer from larger parent sections linked via metadata.
        </p>
      </header>

      <section className="card">
        <h2>1. Ingest document</h2>
        <div style={{ marginBottom: "0.75rem" }}>
          <label>Title</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="e.g. Invoice Terms Policy"
          />
        </div>
        <div>
          <label>Document text</label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste a longer document here. It will be split into parent sections and child chunks."
            rows={6}
          />
        </div>
        <div style={{ marginTop: "0.5rem" }}>
          <button
            onClick={handleIngest}
            disabled={ingestLoading || !title.trim() || !text.trim()}
          >
            {ingestLoading ? "Ingesting…" : "Ingest as parent+children"}
          </button>
        </div>
        {ingestStatus && (
          <p
            className={ingestStatus.startsWith("Created") ? "success" : "error"}
            style={{ marginTop: "0.5rem" }}
          >
            {ingestStatus}
          </p>
        )}
      </section>

      <section className="card">
        <h2>2. Query</h2>
        <label>Question</label>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g. What are the late payment terms?"
        />
        <div className="row" style={{ marginTop: "0.75rem" }}>
          <div>
            <label>Top child chunks</label>
            <input
              type="number"
              min={1}
              max={100}
              value={topChildren}
              onChange={(e) => setTopChildren(Number(e.target.value) || 30)}
              style={{ width: "5rem" }}
            />
          </div>
          <div>
            <label>Max parents in context</label>
            <input
              type="number"
              min={1}
              max={10}
              value={maxParents}
              onChange={(e) => setMaxParents(Number(e.target.value) || 4)}
              style={{ width: "5rem" }}
            />
          </div>
          <div className="row" style={{ alignItems: "center" }}>
            <input
              id="gen-answer"
              type="checkbox"
              checked={generateAnswer}
              onChange={(e) => setGenerateAnswer(e.target.checked)}
            />
            <label htmlFor="gen-answer">Generate answer</label>
          </div>
        </div>
        <div style={{ marginTop: "0.75rem" }}>
          <button onClick={handleQuery} disabled={queryLoading || !query.trim()}>
            {queryLoading ? "Running…" : "Run parent-aware query"}
          </button>
        </div>
        {queryError && (
          <p className="error" style={{ marginTop: "0.5rem" }}>
            {queryError}
          </p>
        )}
      </section>

      {result && (
        <section className="card">
          <h2>3. Results</h2>
          <p className="muted">Query: “{result.query}”</p>
          <div className="two-cols" style={{ marginTop: "0.8rem" }}>
            <div>
              <h3>Child hits (retrieval units)</h3>
              <ChildList childrenHits={result.children} />
            </div>
            <div>
              <h3>Parent sections (context for LLM)</h3>
              <ParentList parents={result.parents} />
            </div>
          </div>
          {result.answer && (
            <div style={{ marginTop: "1rem" }}>
              <h3>Answer</h3>
              <div className="parent-block">{result.answer}</div>
            </div>
          )}
        </section>
      )}

      <footer className="muted" style={{ marginTop: "2rem", fontSize: "0.8rem" }}>
        Project 10 · Parent Document Retrieval
      </footer>
    </div>
  );
}

