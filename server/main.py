"""FastMCP server entry point with tool definitions."""

import os
from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("Semantic Search")


@mcp.tool(
    annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": True}
)
def index_folder(
    folder_path: Annotated[str, Field(description="Absolute path to the folder to index")],
    file_types: Annotated[
        list[str] | None,
        Field(
            description="File extensions to index, e.g. ['.pdf', '.md']. "
                        "Defaults to all supported types: .txt, .md",
            default=None,
        ),
    ] = None,
    recursive: Annotated[
        bool,
        Field(description="Whether to index subdirectories recursively", default=True),
    ] = True,
) -> dict:
    """Index or re-index all documents in a folder for semantic search.

    Scans the folder for supported document types, extracts text, splits into
    chunks, computes embeddings, and stores them in a local vector database.
    Only processes files that have changed since the last indexing run.
    Safe to call multiple times — unchanged files are skipped automatically.
    """
    from server.indexer import index_folder as _index_folder

    return _index_folder(
        folder_path=folder_path,
        file_types=file_types,
        recursive=recursive,
    )


@mcp.tool(
    annotations={"readOnlyHint": True}
)
def semantic_search(
    query: Annotated[str, Field(description="Natural language search query")],
    folder_path: Annotated[
        str | None,
        Field(
            description="Limit search to a specific indexed folder. "
                        "If omitted, searches all indexed folders.",
            default=None,
        ),
    ] = None,
    top_k: Annotated[
        int,
        Field(description="Number of results to return", default=10, ge=1, le=50),
    ] = 10,
    file_type: Annotated[
        str | None,
        Field(
            description="Filter results by file extension, e.g. '.pdf'",
            default=None,
        ),
    ] = None,
) -> dict:
    """Search indexed documents using natural language.

    Finds the most relevant document chunks matching the query using
    semantic similarity. Returns ranked results with source file paths
    and relevance scores.

    The folder must be indexed first with index_folder.
    """
    from server.search import semantic_search as _semantic_search

    return _semantic_search(
        query=query,
        folder_path=folder_path,
        top_k=top_k,
        file_type=file_type,
    )


def run():
    mcp.run()


if __name__ == "__main__":
    run()
