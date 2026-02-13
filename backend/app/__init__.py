"""
Parent Document Retrieval backend.

Key ideas:
- Ingest raw documents into larger parent sections.
- Split parents into smaller child chunks for vector retrieval.
- At query time, retrieve children, then expand back to parents for context.
"""

