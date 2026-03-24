---
name: semantic-search
description: Search local document folders using natural language. Use when the user
  asks about content in their files, references documents they've mentioned before,
  asks "what does the report say about...", "find the document about...", "was ist in
  dem Dokument uber...", or when they need to locate information across many files.
  Also use when the user asks to index or search a folder of documents.
argument-hint: "<search query or folder path>"
---

# Semantic Document Search

Search across locally indexed document folders using natural language queries.
Supports Markdown and text files (PDF, Word, PowerPoint coming in Phase 2).

## When to Use

**Search automatically** when the user:
- Asks about content that likely lives in their documents
- References reports, notes, emails, or files by topic
- Says things like "find...", "what did ... say about...", "where is the info about..."
- Uses German phrases like "was steht in...", "finde das Dokument uber...",
  "was sagt der Bericht zu..."
- Asks to compare information across multiple documents

**Index first** when the user:
- Mentions a folder of documents they want to search
- Says "index my documents", "make these searchable"
- References a folder that hasn't been indexed yet

## Workflow

### First-time setup
1. Ask which folder(s) the user wants to make searchable
2. Call `index_folder` with the folder path
3. Report results: how many files indexed, any failures
4. Confirm they can now search with natural language

### Searching
1. Call `semantic_search` with the user's query
2. If results are found:
   - Synthesize an answer from the most relevant chunks
   - Always cite the source file and page number (if PDF)
   - Quote relevant passages when helpful
   - Mention the relevance score only if the user asks about confidence
3. If no results:
   - Suggest indexing the relevant folder
   - Suggest rephrasing the query or broadening search terms

### Presenting results
- Lead with the answer, not the search mechanics
- Cite sources naturally: "According to Q3-report.pdf (page 12)..."
- For German queries, respond in German with source citations
- If multiple documents are relevant, synthesize across them
- Offer to show more results or search with different terms

## Important Notes
- The search works in both English and German (and 48 other languages)
- Documents must be indexed before they can be searched
- Indexing is incremental — only changed files are re-processed
- Large folders (1000+ files) may take a few minutes to index initially
