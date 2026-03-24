---
name: Cowork RAG Plugin
description: Local semantic search Claude Code plugin — tech stack, architecture, and implementation status
type: project
---

Claude Code plugin for local semantic search over document folders. Fully offline after initial model download.

**Phase 1 MVP (completed 2026-03-24):** Plugin scaffolding, FastMCP server with `index_folder` + `semantic_search` tools, .txt/.md parsing, RecursiveCharacterTextSplitter chunking, paraphrase-multilingual-MiniLM-L12-v2 embeddings (lazy-loaded), LanceDB vector store, SHA-256 incremental indexing, 38 passing tests.

**Why:** Omar wants a local, offline, open-source RAG solution that works with German + English documents via Claude Code plugin system.

**How to apply:** Phase 2 adds PDF/DOCX/PPTX/CSV parsers, hybrid search (FTS + vector via RRF), `get_index_status` and `reindex_file` tools. Phase 3 covers ONNX runtime, performance, and marketplace publishing. Python 3.13 required (system python is 3.9, use /opt/homebrew/bin/python3.13).
