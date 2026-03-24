---
name: index
description: Index a folder of documents for semantic search
argument-hint: "<folder path>"
---

Index the specified folder for semantic search. This scans all supported document files,
extracts text, and stores embeddings in a local vector database.

Call the `index_folder` tool with the provided folder path. Report the results including
how many files were indexed, skipped, and any errors encountered.
