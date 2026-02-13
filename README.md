# 📎 Parent-Document Retrieval

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.109+-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/ChromaDB-0.4+-FF6F00?style=flat-square" />
</p>

> **Small chunks for retrieval, large parents for context** — Retrieve on precise child chunks, then expand to full parent sections for the LLM. Best of both worlds.

Part of the [Mastering RAG](https://github.com/kishore2797/mastering-rag) ecosystem → tutorial: [rag-07-parent-document-retrieval](https://github.com/kishore2797/rag-07-parent-document-retrieval).

---

## 🌍 Real-World Scenario

> A medical Q&A system indexes clinical guidelines. A doctor asks: "What's the recommended dosage for metformin in elderly patients with renal impairment?" Standard RAG retrieves a tiny chunk: *"adjust dose for renal function."* **Parent-document retrieval** matches that precise sentence, then expands to the full section: dosage tables, contraindications, monitoring. The doctor gets complete guidance, not just a fragment.

---

## 🏗️ What You'll Build

A full-stack RAG app that uses **small child chunks for precise retrieval** and **larger parent sections for rich LLM context**. Children are linked to parents via metadata; you retrieve children, then expand to parents.

```
Standard RAG:             Parent-Document RAG:
┌───────────┐             ┌───────────┐
│ Small     │  retrieve   │ Small     │  retrieve      ┌──────────────┐
│ chunk     │  ──→ LLM    │ child     │  ──→ expand ──→│ Large parent │──→ LLM
│ = context │             │ chunk     │                 │ section      │
└───────────┘             └───────────┘                 └──────────────┘
Less context              Precise match                  Rich context
```

## 🔑 Key Concepts

- **Parent-child hierarchy** — Documents split at two granularities (small + large)
- **Precision vs. context** — Small chunks match better; large chunks explain better
- **Metadata linking** — Each child stores a reference to its parent
- **Context expansion** — Retrieve children, return parents to the LLM

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.11+ · FastAPI · ChromaDB · Sentence-Transformers · OpenAI |
| Frontend | React 19 · Vite · Tailwind CSS |

## 📁 Project Structure

```
parent-document-retrieval/
├── backend/     # FastAPI: ingestion, parent+child chunking, parent-aware retrieval, RAG
├── frontend/    # React + Vite: ingest docs, run queries, inspect children vs parents
└── README.md
```

## 🚀 Quick Start

### Backend

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # Optional: OPENAI_API_KEY for real answers
uvicorn app.main:app --reload --port 8003
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Dev UI: **http://localhost:5177** — proxy `/api` to backend 8003.

## ✨ Features

- **Parent-child chunking** — Small chunks (children) for retrieval; large sections (parents) for context
- **Metadata linking** — Children store parent ID; retrieval returns expanded parent content
- **Compare modes** — Toggle standard vs. parent-document retrieval and compare answers
- **Full RAG** — Optional LLM answer from retrieved (expanded) context
