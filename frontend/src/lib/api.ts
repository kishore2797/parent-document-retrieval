import axios from "axios";

const baseURL = import.meta.env.VITE_API_BASE_URL ?? "/api";

export const api = axios.create({
  baseURL,
  headers: { "Content-Type": "application/json" },
});

export interface ParentDocumentInput {
  title: string;
  text: string;
  doc_id?: string;
}

export interface IngestRequest {
  documents: ParentDocumentInput[];
}

export interface IngestResponse {
  parents_created: number;
  children_created: number;
}

export interface ChildHit {
  id: string;
  parent_id: string;
  doc_id: string;
  title?: string | null;
  score: number;
  snippet: string;
  metadata: Record<string, unknown>;
}

export interface ParentContext {
  parent_id: string;
  doc_id: string;
  title?: string | null;
  score: number;
  text: string;
}

export interface QueryRequest {
  query: string;
  top_children?: number | null;
  max_parents?: number | null;
  generate_answer?: boolean;
}

export interface QueryResponse {
  query: string;
  children: ChildHit[];
  parents: ParentContext[];
  answer: string | null;
}

